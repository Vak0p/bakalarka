from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QGridLayout, QHBoxLayout, QLabel, QSizePolicy,
                               QVBoxLayout, QWidget)

from backend.video import VideoInfo

MUTED_COLOR = "#9A9AA0"
FIELDS = ("Resolution", "Frame rate", "Duration", "File size")


def _format_duration(seconds: float) -> str:
    total = round(seconds)
    hours, rest = divmod(total, 3600)
    minutes, secs = divmod(rest, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def _format_size(size_bytes: int) -> str:
    if size_bytes >= 1024 ** 3:
        return f"{size_bytes / 1024 ** 3:.2f} GB"
    return f"{size_bytes / 1024 ** 2:.1f} MB"


class _ElidedLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._full_text = ""
        self.setTextFormat(Qt.TextFormat.PlainText)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)

    def set_full_text(self, text: str):
        self._full_text = text
        self.setToolTip(text)
        self._elide()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._elide()

    def _elide(self):
        elided = self.fontMetrics().elidedText(
            self._full_text, Qt.TextElideMode.ElideMiddle, self.width()
        )
        if elided != self.text():
            self.setText(elided)


class VideoInfoCard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._name = _ElidedLabel()
        font = self._name.font()
        font.setBold(True)
        self._name.setFont(font)

        self._path = _ElidedLabel()
        self._path.setStyleSheet(f"color: {MUTED_COLOR};")

        self._values: dict[str, QLabel] = {}
        grid = QGridLayout()
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(4)
        grid.setColumnMinimumWidth(2, 28)
        for index, field in enumerate(FIELDS):
            row, pair = divmod(index, 2)
            column = pair * 3
            key = QLabel(field)
            key.setStyleSheet(f"color: {MUTED_COLOR};")
            value = QLabel()
            self._values[field] = value
            grid.addWidget(key, row, column)
            grid.addWidget(value, row, column + 1)

        grid_row = QHBoxLayout()
        grid_row.addStretch(1)
        grid_row.addLayout(grid)
        grid_row.addStretch(1)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 8, 0, 8)
        layout.setSpacing(4)
        layout.addWidget(self._name)
        layout.addWidget(self._path)
        layout.addSpacing(6)
        layout.addLayout(grid_row)

    def set_info(self, info: VideoInfo):
        self._name.set_full_text(info.path.name)
        self._path.set_full_text(str(info.path.absolute()))
        values = {
            "Resolution": f"{info.width} × {info.height}",
            "Frame rate": f"{round(info.fps, 2):g} fps",
            "Duration": _format_duration(info.duration_s),
            "File size": _format_size(info.size_bytes),
        }
        for field, text in values.items():
            self._values[field].setText(text)