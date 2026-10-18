from functools import partial

from PySide6.QtCore import QEvent, QObject, QThreadPool, QTimer, Signal, Slot
from PySide6.QtWidgets import (QFileDialog, QHBoxLayout, QMessageBox, QPushButton,
                               QSizePolicy, QWidget)

from backend.video import SUPPORTED_EXTENSIONS, VideoError, VideoInfo, VideoSource
from frontend.widgets.frame_player import FramePlayer
from frontend.widgets.video_info_card import VideoInfoCard
from frontend.workers import PreviewWorker

PREVIEW_FRAMES = 100
PREVIEW_MAX_WIDTH = 480
LOADING_TOOLTIP = "Available once the video preview has finished loading"

CONTINUE_BUTTON_STYLE = """
QPushButton {
    background-color: transparent;
    color: #C38B6B;
    border: 2px solid #C38B6B;
    border-radius: 5px;
    font-weight: bold;
    padding: 10px;
}
QPushButton:hover {
    background-color: rgba(195, 139, 107, 40);
    color: #D49D7E;
    border-color: #D49D7E;
}
QPushButton:disabled {
    background-color: transparent;
    color: #5B5B60;
    border-color: #3A3B3F;
}
"""

SECONDARY_BUTTON_STYLE = """
QPushButton {
    background-color: #3A3B3F;
    color: #E8E8E8;
    border: none;
    border-radius: 5px;
    font-weight: normal;
    padding: 7px 12px;
}
QPushButton:hover {
    background-color: #4A4B50;
}
QPushButton:pressed {
    background-color: #2B2C30;
}
"""


def _spacer_state(spacer):
    size = spacer.sizeHint()
    policy = spacer.sizePolicy()
    return size.width(), size.height(), policy.horizontalPolicy(), policy.verticalPolicy()


class UploadPageController(QObject):
    video_loaded = Signal(object)
    video_removed = Signal()
    continue_requested = Signal()

    def __init__(self, window, ui):
        super().__init__(window)
        self._window = window
        self._ui = ui
        self._worker: PreviewWorker | None = None
        self._job_id = 0
        self.info: VideoInfo | None = None

        self._spacers = [ui.v_spacer_1, ui.v_spacer_2]
        self._default_spacers = [_spacer_state(spacer) for spacer in self._spacers]

        self._player = FramePlayer()
        self._player.hide()

        self._continue_button = QPushButton("CONTINUE TO VIDEO TRIMMING")
        self._continue_button.setStyleSheet(CONTINUE_BUTTON_STYLE)
        self._continue_button.hide()

        self._info_card = VideoInfoCard()
        self._info_card.hide()

        self._remove_button = QPushButton("Remove video")
        self._replace_button = QPushButton("Upload different video")
        self._secondary_row = QWidget()
        row_layout = QHBoxLayout(self._secondary_row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.addWidget(self._remove_button, 1)
        row_layout.addWidget(self._replace_button, 1)
        self._secondary_row.setStyleSheet(SECONDARY_BUTTON_STYLE)
        self._secondary_row.hide()

        zone_layout = ui.drag_and_drop_zone.layout()
        zone_layout.insertWidget(0, self._player, 1)
        zone_layout.insertWidget(1, self._continue_button)
        zone_layout.insertWidget(2, self._info_card)
        zone_layout.insertWidget(zone_layout.indexOf(ui.upload_button) + 1, self._secondary_row)

        formats = ", ".join(ext.lstrip(".").upper() for ext in SUPPORTED_EXTENSIONS)
        ui.formats_label.setText(f"Supported video formats: {formats}")

        ui.drag_and_drop_zone.setAcceptDrops(True)
        ui.drag_and_drop_zone.installEventFilter(self)
        ui.upload_button.clicked.connect(self._choose_file)
        self._continue_button.clicked.connect(self.continue_requested)
        self._replace_button.clicked.connect(self._choose_file)
        self._remove_button.clicked.connect(self._remove_video)

    def eventFilter(self, watched, event):
        if watched is self._ui.drag_and_drop_zone:
            event_type = event.type()
            if event_type in (QEvent.Type.DragEnter, QEvent.Type.DragMove):
                if event.mimeData().hasUrls():
                    event.acceptProposedAction()
                    return True
            elif event_type == QEvent.Type.Drop:
                urls = event.mimeData().urls()
                if urls:
                    event.acceptProposedAction()
                    QTimer.singleShot(0, partial(self.load_video, urls[0].toLocalFile()))
                    return True
        return super().eventFilter(watched, event)

    def load_video(self, path: str):
        try:
            with VideoSource(path) as source:
                info = source.info
        except VideoError as error:
            QMessageBox.warning(self._window, "Cannot load video", str(error))
            return

        self._cancel_preview()
        self.info = info
        self._show_video_info(info)
        self._player.begin(PREVIEW_FRAMES)
        self._player.show()

        worker = PreviewWorker(self._job_id, str(info.path), PREVIEW_FRAMES, PREVIEW_MAX_WIDTH)
        worker.signals.frame_ready.connect(self._on_frame)
        worker.signals.finished.connect(self._on_finished)
        worker.signals.failed.connect(self._on_failed)
        self._worker = worker
        QThreadPool.globalInstance().start(worker)

        self.video_loaded.emit(info)

    def shutdown(self):
        self._cancel_preview()

    def _show_video_info(self, info: VideoInfo):
        ui = self._ui
        ui.video_icon_label.hide()
        ui.drop_here_label.hide()
        ui.upload_button.hide()
        for spacer in self._spacers:
            spacer.changeSize(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        ui.drag_and_drop_zone.layout().invalidate()

        self._info_card.set_info(info)
        self._info_card.show()
        self._secondary_row.show()

        self._continue_button.setEnabled(False)
        self._continue_button.setToolTip(LOADING_TOOLTIP)
        self._continue_button.show()

    def _remove_video(self):
        self._cancel_preview()
        self.info = None
        self._player.clear()
        self._player.hide()
        self._continue_button.hide()
        self._info_card.hide()
        self._secondary_row.hide()

        ui = self._ui
        ui.video_icon_label.show()
        ui.drop_here_label.show()
        ui.upload_button.show()
        for spacer, state in zip(self._spacers, self._default_spacers):
            spacer.changeSize(*state)
        ui.drag_and_drop_zone.layout().invalidate()
        self.video_removed.emit()

    def _choose_file(self):
        extensions = " ".join(f"*{ext}" for ext in SUPPORTED_EXTENSIONS)
        path, _ = QFileDialog.getOpenFileName(
            self._window, "Choose video file", "", f"Video files ({extensions})"
        )
        if path:
            self.load_video(path)

    def _cancel_preview(self):
        self._job_id += 1
        if self._worker:
            self._worker.cancel()
            self._worker = None

    @Slot(int, object)
    def _on_frame(self, job_id, frame):
        if job_id == self._job_id:
            self._player.add_frame(frame)

    @Slot(int)
    def _on_finished(self, job_id):
        if job_id == self._job_id:
            self._player.finish()
            self._continue_button.setEnabled(True)
            self._continue_button.setToolTip("")

    @Slot(int, str)
    def _on_failed(self, job_id, message):
        if job_id == self._job_id:
            self._player.finish()
            QMessageBox.warning(self._window, "Preview failed", message)