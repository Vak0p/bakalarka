from __future__ import annotations

import hashlib
import os
import shutil
from collections.abc import Iterable, Sequence
from pathlib import Path

import cv2
import numpy as np

from backend.video import PreviewFrame, VideoInfo

JPEG_QUALITY = 85
COMPLETE_MARKER = ".complete"


class PreviewCache:
    def __init__(self, root: Path):
        self._root = root

    def save(self, info: VideoInfo, frames: Sequence[PreviewFrame]) -> None:
        try:
            folder = self._folder(info)
            shutil.rmtree(folder, ignore_errors=True)
            folder.mkdir(parents=True, exist_ok=True)
            for frame in frames:
                bgr = cv2.cvtColor(frame.image, cv2.COLOR_RGB2BGR)
                ok, buffer = cv2.imencode(".jpg", bgr, [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY])
                if ok:
                    (folder / f"{frame.index}.jpg").write_bytes(buffer.tobytes())
            (folder / COMPLETE_MARKER).touch()
        except OSError:
            pass

    def load(self, info: VideoInfo) -> list[PreviewFrame]:
        try:
            folder = self._folder(info)
            if not (folder / COMPLETE_MARKER).exists():
                return []
            frames = []
            for path in sorted(folder.glob("*.jpg"), key=lambda p: int(p.stem)):
                data = np.frombuffer(path.read_bytes(), dtype=np.uint8)
                bgr = cv2.imdecode(data, cv2.IMREAD_COLOR)
                if bgr is None:
                    return []
                index = int(path.stem)
                time_s = index / info.fps if info.fps > 0 else 0.0
                frames.append(PreviewFrame(index, time_s, cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)))
            return frames
        except (OSError, ValueError):
            return []

    def delete(self, info: VideoInfo) -> None:
        try:
            shutil.rmtree(self._folder(info), ignore_errors=True)
        except OSError:
            pass

    def prune(self, keep: Iterable[VideoInfo]) -> None:
        wanted = set()
        for info in keep:
            try:
                wanted.add(self._folder(info).name)
            except OSError:
                pass
        if not self._root.is_dir():
            return
        for folder in self._root.iterdir():
            if folder.is_dir() and folder.name not in wanted:
                shutil.rmtree(folder, ignore_errors=True)

    def _folder(self, info: VideoInfo) -> Path:
        stat = info.path.stat()
        raw = f"{os.path.normcase(os.path.abspath(info.path))}|{stat.st_size}|{stat.st_mtime_ns}"
        return self._root / hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]