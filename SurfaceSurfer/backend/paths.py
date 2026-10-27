import os
from pathlib import Path

APP_DIR_NAME = "SurfaceSurfer"


def data_dir() -> Path:
    base = (
        os.environ.get("LOCALAPPDATA")
        or os.environ.get("XDG_DATA_HOME")
        or Path.home() / ".local" / "share"
    )
    return Path(base) / APP_DIR_NAME