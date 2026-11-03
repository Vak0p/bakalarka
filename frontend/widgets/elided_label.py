from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QSizePolicy


class ElidedLabel(QLabel):
    def __init__(self, alignment=Qt.AlignmentFlag.AlignCenter, parent=None):
        super().__init__(parent)
        self._full_text = ""
        self.setTextFormat(Qt.TextFormat.PlainText)
        self.setAlignment(alignment)
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