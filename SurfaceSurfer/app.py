import sys

import qdarktheme
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication

from frontend.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    palette = qdarktheme.load_palette(theme="dark")
    palette.setColor(QPalette.ColorRole.Highlight, QColor("#C38B6B"))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#000000"))
    app.setPalette(palette)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()