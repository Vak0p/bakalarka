import sys

import qdarktheme
from PySide6.QtWidgets import QApplication

from frontend.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("dark")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()