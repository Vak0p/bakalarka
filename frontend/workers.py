from PySide6.QtCore import QObject, QRunnable, Signal

from backend.video import VideoError, iter_preview_frames


class PreviewSignals(QObject):
    frame_ready = Signal(int, object)
    finished = Signal(int)
    failed = Signal(int, str)


class PreviewWorker(QRunnable):
    def __init__(self, job_id: int, path: str, count: int, max_width: int):
        super().__init__()
        self.job_id = job_id
        self.path = path
        self.count = count
        self.max_width = max_width
        self.signals = PreviewSignals()
        self._cancelled = False

    def cancel(self):
        self._cancelled = True

    def run(self):
        try:
            for frame in iter_preview_frames(self.path, self.count, self.max_width):
                if self._cancelled:
                    return
                self.signals.frame_ready.emit(self.job_id, frame)
        except VideoError as error:
            self.signals.failed.emit(self.job_id, str(error))
            return
        self.signals.finished.emit(self.job_id)