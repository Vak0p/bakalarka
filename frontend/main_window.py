import ctypes
import sys
from functools import partial

from PySide6.QtWidgets import QMainWindow

from frontend.pages.upload_page import UploadPageController
from frontend.recent_files_controller import RecentFilesController
from ui.main_window_ui import Ui_main_window


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_main_window()
        self.ui.setupUi(self)
        self.setStyleSheet(self.styleSheet())
        self.setWindowTitle("Surface Surfer")
        self._enable_dark_title_bar()

        for name in ["ortho_map_zoneA.json", "highway_scan_2026.json"]:
            self.ui.recent_projects_list.addItem(name)

        self.upload_page = UploadPageController(self, self.ui)
        self.recent_files = RecentFilesController(self.ui.recent_files_list, self)

        self.upload_page.video_loaded.connect(self.recent_files.add)
        self.upload_page.preview_ready.connect(self.recent_files.set_preview)
        self.recent_files.video_selected.connect(self.upload_page.load_cached)

        self._task_buttons = [self.ui.task_button_1, self.ui.task_button_2,
                              self.ui.task_button_3]
        for index, button in enumerate(self._task_buttons):
            button.clicked.connect(partial(self.show_page, index))
        self.upload_page.continue_requested.connect(partial(self.show_page, 1))
        self.ui.back_button.clicked.connect(partial(self.show_page, 0))
        self.ui.continue_to_stitching_button.clicked.connect(partial(self.show_page, 2))
        self.show_page(0)

    def show_page(self, index: int):
        self.ui.page_stack.setCurrentIndex(index)
        self._task_buttons[index].setChecked(True)

    def closeEvent(self, event):
        self.upload_page.shutdown()
        super().closeEvent(event)

    def _enable_dark_title_bar(self):
        if sys.platform == "win32":
            hwnd = int(self.winId())
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(ctypes.c_int(1)), 4)