from PySide6.QtCore import QPoint, QRect, QRectF, QSize, Qt, QTimer
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QSizePolicy,
                               QSlider, QVBoxLayout, QWidget)

from backend.video import PreviewFrame
from frontend.qt_utils import make_media_icon, ndarray_to_pixmap

PLAY_FPS = 10
ACCENT = "#C38B6B"

STYLE = """
QPushButton {
    background-color: #C38B6B;
    color: black;
    font-weight: bold;
    border: none;
    border-radius: 5px;
    padding: 0;
}
QPushButton:hover {
    background-color: #D49D7E;
}
QPushButton:disabled {
    background-color: #3A3B3F;
}
QSlider::groove:horizontal {
    height: 4px;
    background: #3A3B3F;
    border-radius: 2px;
}
QSlider::sub-page:horizontal {
    background: #C38B6B;
    border-radius: 2px;
}
QSlider::handle:horizontal {
    background: #C38B6B;
    width: 14px;
    margin: -5px 0;
    border-radius: 7px;
}
QSlider::handle:horizontal:hover {
    background: #D49D7E;
}
QSlider::sub-page:horizontal:disabled {
    background: #5B5B60;
}
QSlider::handle:horizontal:disabled {
    background: #5B5B60;
}
"""


class _LoadingOverlay(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._progress = 0
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.hide()

    def set_progress(self, percent: int):
        self._progress = percent
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 160))

        middle = self.height() // 2
        painter.setPen(QColor("#FFFFFF"))

        font = painter.font()
        font.setPointSize(26)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(QRect(0, middle - 30, self.width(), 44),
                         Qt.AlignmentFlag.AlignCenter, f"{self._progress}%")

        font.setPointSize(10)
        font.setBold(False)
        painter.setFont(font)
        painter.drawText(QRect(0, middle + 16, self.width(), 22),
                         Qt.AlignmentFlag.AlignCenter, "Loading preview")

        margin = 24
        bar_width = self.width() - 2 * margin
        bar_y = self.height() - 22
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(255, 255, 255, 60))
        painter.drawRoundedRect(QRectF(margin, bar_y, bar_width, 4), 2, 2)
        if self._progress > 0:
            painter.setBrush(QColor(ACCENT))
            painter.drawRoundedRect(
                QRectF(margin, bar_y, bar_width * self._progress / 100, 4), 2, 2
            )


class FramePlayer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._frames: list[PreviewFrame] = []
        self._total = 0
        self._pixmap_size: QSize | None = None
        self._play_icon = make_media_icon("play")
        self._pause_icon = make_media_icon("pause")

        self._image = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        self._image.setMinimumSize(200, 150)
        self._image.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self._overlay = _LoadingOverlay(self._image)

        self._slider = QSlider(Qt.Orientation.Horizontal)
        self._play_button = QPushButton()
        self._play_button.setFixedSize(40, 28)
        self._play_button.setIconSize(QSize(16, 16))
        self._time_label = QLabel("0:00")
        self._time_label.setMinimumWidth(40)
        self._time_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        controls = QHBoxLayout()
        controls.addWidget(self._play_button)
        controls.addWidget(self._slider, 1)
        controls.addWidget(self._time_label)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._image, 1)
        layout.addLayout(controls)

        self.setStyleSheet(STYLE)

        self._timer = QTimer(self)
        self._timer.setInterval(1000 // PLAY_FPS)
        self._timer.timeout.connect(self._advance)
        self._play_button.clicked.connect(self._toggle_play)
        self._slider.valueChanged.connect(self._show)
        self.clear()

    def clear(self):
        self._stop_playback()
        self._frames.clear()
        self._total = 0
        self._pixmap_size = None
        self._image.clear()
        self._overlay.hide()
        self._slider.setRange(0, 0)
        self._slider.setValue(0)
        self._time_label.setText("0:00")
        self._play_button.setEnabled(False)
        self._slider.setEnabled(False)

    def begin(self, total: int):
        self.clear()
        self._total = total
        self._slider.setRange(0, max(total - 1, 0))
        self._overlay.set_progress(0)
        self._overlay.show()
        self._update_overlay()

    def add_frame(self, frame: PreviewFrame):
        self._frames.append(frame)
        if len(self._frames) == 1:
            self._show(0)
        if self._total:
            self._overlay.set_progress(100 * len(self._frames) // self._total)

    def finish(self):
        self._overlay.hide()
        if not self._frames:
            return
        self._slider.setRange(0, len(self._frames) - 1)
        self._slider.setEnabled(True)
        self._play_button.setEnabled(True)
        self._slider.setValue(0)
        self._show(0)
        if len(self._frames) > 1:
            self._start_playback()

    def _show(self, index: int):
        if index >= len(self._frames):
            return
        frame = self._frames[index]
        pixmap = ndarray_to_pixmap(frame.image).scaled(
            self._image.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self._image.setPixmap(pixmap)
        self._pixmap_size = pixmap.size()
        minutes, seconds = divmod(int(frame.time_s), 60)
        self._time_label.setText(f"{minutes}:{seconds:02d}")
        self._update_overlay()

    def _update_overlay(self):
        if self._pixmap_size is None:
            rect = self._image.rect()
        else:
            rect = QRect(QPoint(0, 0), self._pixmap_size)
            rect.moveCenter(self._image.rect().center())
        self._overlay.setGeometry(rect)

    def _start_playback(self):
        self._timer.start()
        self._play_button.setIcon(self._pause_icon)

    def _stop_playback(self):
        self._timer.stop()
        self._play_button.setIcon(self._play_icon)

    def _advance(self):
        self._slider.setValue((self._slider.value() + 1) % len(self._frames))

    def _toggle_play(self):
        if self._timer.isActive():
            self._stop_playback()
        else:
            self._start_playback()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._show(self._slider.value())
        self._update_overlay()