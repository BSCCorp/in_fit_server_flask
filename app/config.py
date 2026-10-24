"""Application configuration."""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Config:
    BASE_URL = os.environ.get("BASE_URL", "").rstrip("/")
    RECEIVER_URL = os.environ.get("RECEIVER_URL", "")
    TITLE = os.environ.get("TITLE", "Flask InFit API")
    VIDEO_DIR = Path(os.environ.get("VIDEO_DIR", str(PROJECT_ROOT / "videos")))
    PUBLIC_DIR = Path(os.environ.get("PUBLIC_DIR", str(PROJECT_ROOT / "public")))
    LOG_FILE = Path(
        os.environ.get("LOG_FILE", str(PROJECT_ROOT / "logs" / "output.log"))
    )
