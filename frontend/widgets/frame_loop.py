from collections.abc import Sequence

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QLabel, QSizePolicy

from backend.video import PreviewFrame
from frontend.qt_utils import ndarray_to_pixmap

LOOP_FPS = 20


class FrameLoop(QLabel):
    def __init__(self, height: int = 150, parent=None):
        super().__init__(parent)
        self._frames: list[PreviewFrame] = []
        self._index = 0
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedHeight(height)
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)

        self._timer = QTimer(self)
        self._timer.setInterval(1000 // LOOP_FPS)
        self._timer.timeout.connect(self._advance)

    def set_frames(self, frames: Sequence[PreviewFrame]):
        self._timer.stop()
        self._frames = list(frames)
        self._index = 0
        self._show()
        if self.isVisible():
            self._play()

    def showEvent(self, event):
        super().showEvent(event)
        self._play()

    def hideEvent(self, event):
        super().hideEvent(event)
        self._timer.stop()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._show()

    def _play(self):
        if len(self._frames) > 1:
            self._timer.start()

    def _advance(self):
        self._index = (self._index + 1) % len(self._frames)
        self._show()

    def _show(self):
        if not self._frames:
            self.clear()
            return
        pixmap = ndarray_to_pixmap(self._frames[self._index].image).scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.setPixmap(pixmap)