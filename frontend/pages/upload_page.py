import html
from functools import partial

from PySide6.QtCore import QEvent, QObject, Qt, QThreadPool, QTimer, Signal, Slot
from PySide6.QtWidgets import QFileDialog, QMessageBox, QSizePolicy

from backend.video import SUPPORTED_EXTENSIONS, VideoError, VideoInfo, VideoSource
from frontend.widgets.frame_player import FramePlayer
from frontend.workers import PreviewWorker

PREVIEW_FRAMES = 100
PREVIEW_MAX_WIDTH = 480
PATH_COLOR = "#9A9AA0"
ZERO_WIDTH_SPACE = "\u200b"


def format_video_info(info: VideoInfo, path: str) -> str:
    wrappable_path = (
        html.escape(path)
        .replace("\\", "\\" + ZERO_WIDTH_SPACE)
        .replace("/", "/" + ZERO_WIDTH_SPACE)
    )
    details = (
        f"{info.width}×{info.height} · {info.fps:.1f} fps · "
        f"{info.duration_s:.0f} s · {info.size_bytes / 1e6:.0f} MB"
    )
    return (
        f"<b>{html.escape(info.path.name)}</b><br>"
        f'<span style="color: {PATH_COLOR};">{wrappable_path}</span><br>'
        f"{details}"
    )


class UploadPageController(QObject):
    video_loaded = Signal(object)

    def __init__(self, window, ui):
        super().__init__(window)
        self._window = window
        self._ui = ui
        self._worker: PreviewWorker | None = None
        self._job_id = 0
        self.info: VideoInfo | None = None

        self._player = FramePlayer()
        self._player.hide()
        ui.drag_and_drop_zone.layout().insertWidget(0, self._player, 1)

        formats = ", ".join(ext.lstrip(".").upper() for ext in SUPPORTED_EXTENSIONS)
        ui.formats_label.setText(f"Supported video formats: {formats}")

        ui.drag_and_drop_zone.setAcceptDrops(True)
        ui.drag_and_drop_zone.installEventFilter(self)
        ui.upload_button.clicked.connect(self._choose_file)

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
        for spacer in (ui.v_spacer_1, ui.v_spacer_2):
            spacer.changeSize(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        ui.drag_and_drop_zone.layout().invalidate()

        path = str(info.path.absolute())
        ui.drop_here_label.setTextFormat(Qt.TextFormat.RichText)
        ui.drop_here_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ui.drop_here_label.setWordWrap(True)
        ui.drop_here_label.setToolTip(path)
        ui.drop_here_label.setText(format_video_info(info, path))

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

    @Slot(int, str)
    def _on_failed(self, job_id, message):
        if job_id == self._job_id:
            self._player.finish()
            QMessageBox.warning(self._window, "Preview failed", message)