import numpy as np
from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QIcon, QImage, QPainter, QPixmap, QPolygonF


def ndarray_to_pixmap(frame: np.ndarray) -> QPixmap:
    frame = np.ascontiguousarray(frame)
    height, width, channels = frame.shape
    image = QImage(frame.data, width, height, channels * width, QImage.Format.Format_RGB888)
    return QPixmap.fromImage(image)


def make_media_icon(kind: str, size: int = 16) -> QIcon:
    icon = QIcon()
    scale = 2
    colors = ((QIcon.Mode.Normal, "#000000"), (QIcon.Mode.Disabled, "#6B6B70"))
    for mode, color in colors:
        pixmap = QPixmap(size * scale, size * scale)
        pixmap.setDevicePixelRatio(scale)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(color))
        if kind == "play":
            painter.drawPolygon(QPolygonF([
                QPointF(size * 0.30, size * 0.15),
                QPointF(size * 0.30, size * 0.85),
                QPointF(size * 0.85, size * 0.50),
            ]))
        else:
            painter.drawRect(QRectF(size * 0.22, size * 0.15, size * 0.20, size * 0.70))
            painter.drawRect(QRectF(size * 0.58, size * 0.15, size * 0.20, size * 0.70))
        painter.end()

        icon.addPixmap(pixmap, mode)
    return icon