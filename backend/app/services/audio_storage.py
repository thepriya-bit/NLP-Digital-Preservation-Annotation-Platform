import os
from pathlib import Path

from app.core.config import settings

AUDIO_DIR = Path(settings.LOCAL_AUDIO_DIR)


def _ensure_dir():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def store_audio_local(file_bytes: bytes, filename: str) -> str:
    _ensure_dir()
    filepath = AUDIO_DIR / filename
    with open(filepath, "wb") as f:
        f.write(file_bytes)
    return f"/audio/{filename}"


def delete_audio_local(audio_url: str) -> bool:
    filename = audio_url.rsplit("/", 1)[-1]
    filepath = AUDIO_DIR / filename
    if filepath.exists():
        filepath.unlink()
        return True
    return False


def list_all_local_audio() -> list[dict]:
    _ensure_dir()
    files = []
    for f in AUDIO_DIR.iterdir():
        if f.is_file():
            files.append({"name": f.name, "path": f"/audio/{f.name}"})
    return files
