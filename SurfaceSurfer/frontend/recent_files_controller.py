from functools import partial

from PySide6.QtCore import QObject, QSize, Qt, QTimer, Signal, Slot
from PySide6.QtWidgets import QAbstractItemView, QListWidget, QListWidgetItem

from backend.paths import data_dir
from backend.recent_files import RecentFile, RecentFiles
from backend.video import VideoInfo
from frontend.widgets.recent_file_entry import RecentFileEntry


class RecentFilesController(QObject):
    video_selected = Signal(object, object)

    def __init__(self, list_widget: QListWidget, parent=None):
        super().__init__(parent)
        self._list = list_widget
        self._store = RecentFiles(data_dir())
        self._expanded_key: str | None = None
        self._row_height: int | None = None

        list_widget.clear()
        list_widget.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        list_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        list_widget.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        list_widget.itemClicked.connect(self._on_item_clicked)
        self._rebuild()

    @Slot(object)
    def add(self, info: VideoInfo):
        self._store.add(info)
        self._expanded_key = None
        self._rebuild()

    @Slot(object, object)
    def set_preview(self, info: VideoInfo, frames):
        if self._store.set_frames(info, frames) is not None:
            self._rebuild()

    def _rebuild(self):
        scroll = self._list.verticalScrollBar().value()
        self._list.clear()
        expanded = False
        for entry in self._store.items:
            item = QListWidgetItem(entry.info.path.name)
            item.setData(Qt.ItemDataRole.UserRole, entry.key)
            item.setToolTip(str(entry.info.path.absolute()))
            self._list.addItem(item)
            if entry.key == self._expanded_key:
                self._expand(item, entry)
                expanded = True

        if expanded:
            QTimer.singleShot(0, partial(self._scroll_to, self._expanded_key))
        else:
            self._list.verticalScrollBar().setValue(scroll)

    def _expand(self, item: QListWidgetItem, entry: RecentFile):
        widget = RecentFileEntry(self._plain_row_height(), self._list.fontMetrics().height())
        widget.setFont(self._list.font())
        widget.set_info(entry.info)
        widget.set_frames(self._store.frames_for(entry))
        widget.header_clicked.connect(partial(self._toggle_later, entry.key))
        widget.cancel_requested.connect(partial(self._toggle_later, entry.key))
        widget.upload_requested.connect(partial(self._upload, entry.key))
        widget.remove_requested.connect(partial(self._remove_later, entry.key))

        item.setText("")
        item.setSizeHint(QSize(0, widget.sizeHint().height()))
        self._list.setItemWidget(item, widget)

    def _plain_row_height(self) -> int:
        if self._row_height is not None:
            return self._row_height
        probe = QListWidgetItem("Ag")
        self._list.addItem(probe)
        height = self._list.sizeHintForRow(self._list.row(probe))
        self._list.takeItem(self._list.row(probe))
        if height <= 0:
            return self._list.fontMetrics().height() + 8
        self._row_height = height
        return height

    def _scroll_to(self, key: str):
        for row in range(self._list.count()):
            item = self._list.item(row)
            if item.data(Qt.ItemDataRole.UserRole) == key:
                self._list.scrollToItem(item, QAbstractItemView.ScrollHint.PositionAtTop)
                return

    def _on_item_clicked(self, item: QListWidgetItem):
        key = item.data(Qt.ItemDataRole.UserRole)
        if key:
            self._toggle(key)

    def _toggle_later(self, key: str):
        QTimer.singleShot(0, partial(self._toggle, key))

    def _toggle(self, key: str):
        self._expanded_key = None if self._expanded_key == key else key
        self._rebuild()

    def _remove_later(self, key: str):
        QTimer.singleShot(0, partial(self._remove, key))

    def _remove(self, key: str):
        self._store.remove(key)
        if self._expanded_key == key:
            self._expanded_key = None
        self._rebuild()

    def _upload(self, key: str):
        entry = self._store.get(key)
        if entry is not None:
            frames = list(self._store.frames_for(entry))
            QTimer.singleShot(0, partial(self.video_selected.emit, entry.info, frames))