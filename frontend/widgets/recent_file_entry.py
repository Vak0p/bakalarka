from collections.abc import Sequence

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from backend.video import PreviewFrame, VideoInfo
from frontend.widgets.elided_label import ElidedLabel
from frontend.widgets.frame_loop import FrameLoop

ACCENT = "#C38B6B"
MUTED = "#9A9AA0"
PREVIEW_MAX_HEIGHT = 120
BUTTON_HEIGHT = 28
SPACING = 4
HEADER_INSET = 3
RIGHT_MARGIN = 4
BOTTOM_MARGIN = 6

RESET_STYLE = """
QLabel {
    padding: 0;
    margin: 0;
    border: none;
    background: transparent;
}
"""

REMOVE_BUTTON_STYLE = """
QPushButton {
    background: transparent;
    color: #9A9AA0;
    border: none;
    padding: 0 2px;
    font-weight: normal;
}
QPushButton:hover {
    color: #E8E8E8;
}
"""

UPLOAD_BUTTON_STYLE = """
QPushButton {
    background-color: #C38B6B;
    color: black;
    font-weight: bold;
    border: none;
    border-radius: 5px;
    padding: 0 8px;
}
QPushButton:hover {
    background-color: #D49D7E;
}
"""

CANCEL_BUTTON_STYLE = """
QPushButton {
    background-color: #3A3B3F;
    color: #E8E8E8;
    border: none;
    border-radius: 5px;
    font-weight: normal;
    padding: 0 8px;
}
QPushButton:hover {
    background-color: #4A4B50;
}
"""

LEFT_CENTER = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter


class RecentFileEntry(QWidget):
    header_clicked = Signal()
    upload_requested = Signal()
    cancel_requested = Signal()
    remove_requested = Signal()

    def __init__(self, row_height: int, text_height: int, parent=None):
        super().__init__(parent)
        top_padding = max(0, (row_height - text_height) // 2)
        self._header_hit_height = top_padding + text_height + SPACING
        self.setStyleSheet(RESET_STYLE)

        self._name = ElidedLabel(LEFT_CENTER)
        self._name.setFixedHeight(text_height)
        self._name.setStyleSheet(f"color: {ACCENT};")

        remove_button = QPushButton("Remove")
        remove_button.setStyleSheet(REMOVE_BUTTON_STYLE)
        remove_button.setFixedHeight(text_height)
        remove_button.setCursor(Qt.CursorShape.PointingHandCursor)
        remove_button.clicked.connect(self.remove_requested)

        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)
        header.setSpacing(6)
        header.addWidget(self._name, 1)
        header.addWidget(remove_button)

        self._preview = FrameLoop(PREVIEW_MAX_HEIGHT)

        self._status = QLabel("Preview is not available yet")
        self._status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._status.setFixedHeight(PREVIEW_MAX_HEIGHT)
        self._status.setStyleSheet(f"color: {MUTED};")

        self._path = ElidedLabel(LEFT_CENTER)
        self._path.setFixedHeight(text_height)
        self._path.setStyleSheet(f"color: {MUTED};")

        upload_button = QPushButton("Upload this video")
        upload_button.setStyleSheet(UPLOAD_BUTTON_STYLE)
        upload_button.setFixedHeight(BUTTON_HEIGHT)
        upload_button.clicked.connect(self.upload_requested)
        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet(CANCEL_BUTTON_STYLE)
        cancel_button.setFixedHeight(BUTTON_HEIGHT)
        cancel_button.clicked.connect(self.cancel_requested)

        buttons = QHBoxLayout()
        buttons.setSpacing(6)
        buttons.addWidget(upload_button, 2)
        buttons.addWidget(cancel_button, 1)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(HEADER_INSET, top_padding, RIGHT_MARGIN, BOTTOM_MARGIN)
        layout.setSpacing(SPACING)
        layout.addLayout(header)
        layout.addWidget(self._preview)
        layout.addWidget(self._status)
        layout.addWidget(self._path)
        layout.addLayout(buttons)
        layout.addStretch(1)

    def set_info(self, info: VideoInfo):
        self._name.set_full_text(info.path.name)
        self._path.set_full_text(str(info.path.absolute()))

    def set_frames(self, frames: Sequence[PreviewFrame]):
        has_frames = bool(frames)
        self._preview.setVisible(has_frames)
        self._status.setVisible(not has_frames)
        if has_frames:
            self._preview.set_frames(frames)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if event.position().y() < self._header_hit_height:
                self.header_clicked.emit()
        event.accept()