from __future__ import annotations

import json
import os
import threading
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path

from backend.preview_cache import PreviewCache
from backend.video import PreviewFrame, VideoError, VideoInfo, VideoSource

MAX_RECENT_FILES = 5
LIST_FILE_NAME = "recent_files.json"


def file_key(info: VideoInfo) -> str:
    return os.path.normcase(os.path.abspath(info.path))


@dataclass(eq=False)
class RecentFile:
    info: VideoInfo
    frames: list[PreviewFrame] = field(default_factory=list)

    @property
    def key(self) -> str:
        return file_key(self.info)


class RecentFiles:
    def __init__(self, storage_dir: Path | None = None, limit: int = MAX_RECENT_FILES):
        self._limit = limit
        self._items: list[RecentFile] = []
        self._list_path: Path | None = None
        self._cache: PreviewCache | None = None
        if storage_dir is not None:
            self._list_path = storage_dir / LIST_FILE_NAME
            self._cache = PreviewCache(storage_dir / "previews")
            self._load()

    @property
    def items(self) -> list[RecentFile]:
        return list(self._items)

    def get(self, key: str) -> RecentFile | None:
        return next((item for item in self._items if item.key == key), None)

    def add(self, info: VideoInfo) -> RecentFile:
        entry = self.get(file_key(info))
        if entry is None:
            entry = RecentFile(info)
        else:
            self._items.remove(entry)
            if entry.info != info:
                entry.frames = []
            entry.info = info
        self._items.insert(0, entry)

        evicted = self._items[self._limit:]
        del self._items[self._limit:]
        for old in evicted:
            self._delete_preview(old)
        self._save_list()
        return entry

    def remove(self, key: str) -> None:
        entry = self.get(key)
        if entry is None:
            return
        self._items.remove(entry)
        self._delete_preview(entry)
        self._save_list()

    def set_frames(self, info: VideoInfo,
                   frames: Sequence[PreviewFrame]) -> RecentFile | None:
        entry = self.get(file_key(info))
        if entry is None:
            return None
        entry.frames = list(frames)
        if self._cache is not None:
            threading.Thread(
                target=self._cache.save, args=(entry.info, entry.frames), daemon=True
            ).start()
        return entry

    def frames_for(self, entry: RecentFile) -> list[PreviewFrame]:
        if not entry.frames and self._cache is not None:
            entry.frames = self._cache.load(entry.info)
        return entry.frames

    def _delete_preview(self, entry: RecentFile) -> None:
        if self._cache is not None:
            self._cache.delete(entry.info)

    def _load(self) -> None:
        try:
            data = json.loads(self._list_path.read_text(encoding="utf-8"))
            paths = [str(path) for path in data.get("files", [])]
        except (OSError, ValueError, AttributeError):
            paths = []

        for path in paths[:self._limit]:
            try:
                with VideoSource(path) as source:
                    self._items.append(RecentFile(source.info))
            except VideoError:
                continue

        self._cache.prune(item.info for item in self._items)
        self._save_list()

    def _save_list(self) -> None:
        if self._list_path is None:
            return
        payload = {"files": [str(item.info.path.absolute()) for item in self._items]}
        try:
            self._list_path.parent.mkdir(parents=True, exist_ok=True)
            temp = self._list_path.with_suffix(".tmp")
            temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            temp.replace(self._list_path)
        except OSError:
            pass