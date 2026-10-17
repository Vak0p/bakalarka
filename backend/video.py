from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

import cv2
import numpy as np

SUPPORTED_EXTENSIONS = (".mp4", ".mov", ".avi", ".mkv", ".webm")


class VideoError(Exception):
    pass


@dataclass(frozen=True)
class VideoInfo:
    path: Path
    width: int
    height: int
    fps: float
    frame_count: int
    size_bytes: int

    @property
    def duration_s(self) -> float:
        return self.frame_count / self.fps if self.fps > 0 else 0.0


@dataclass(frozen=True)
class PreviewFrame:
    index: int
    time_s: float
    image: np.ndarray


class VideoSource:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        if not self.path.is_file():
            raise VideoError(f"File does not exist: {self.path}")
        if self.path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            raise VideoError(f"Unsupported format: {self.path.suffix}")

        self._cap = cv2.VideoCapture(str(self.path))
        if not self._cap.isOpened():
            raise VideoError(f"Could not open video: {self.path.name}")

        self.info = VideoInfo(
            path=self.path,
            width=int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            height=int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            fps=self._cap.get(cv2.CAP_PROP_FPS),
            frame_count=int(self._cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            size_bytes=self.path.stat().st_size,
        )
        if self.info.frame_count <= 0:
            self._cap.release()
            raise VideoError("Could not determine the number of frames")

    def read_frame(self, index: int) -> np.ndarray:
        index = max(0, min(index, self.info.frame_count - 1))
        self._cap.set(cv2.CAP_PROP_POS_FRAMES, index)
        ok, frame = self._cap.read()
        if not ok:
            raise VideoError(f"Could not read frame {index}")
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def close(self) -> None:
        self._cap.release()

    def __enter__(self) -> VideoSource:
        return self

    def __exit__(self, *exc) -> None:
        self.close()


def _downscale(image: np.ndarray, max_width: int) -> np.ndarray:
    height, width = image.shape[:2]
    if width <= max_width:
        return image
    size = (max_width, round(height * max_width / width))
    return cv2.resize(image, size, interpolation=cv2.INTER_AREA)


def iter_preview_frames(path: str | Path, count: int = 100,
                        max_width: int = 480) -> Iterator[PreviewFrame]:
    with VideoSource(path) as source:
        info = source.info
        count = min(count, info.frame_count)
        for i in range(count):
            index = int((i + 0.5) * info.frame_count / count)
            image = _downscale(source.read_frame(index), max_width)
            time_s = index / info.fps if info.fps > 0 else 0.0
            yield PreviewFrame(index, time_s, image)