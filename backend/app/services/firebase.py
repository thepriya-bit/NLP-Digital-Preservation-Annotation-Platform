import os
from pathlib import Path

from app.core.config import settings
from app.services.audio_storage import (
    delete_audio_local,
    list_all_local_audio,
    store_audio_local,
)

USE_FIREBASE = bool(settings.FIREBASE_CREDENTIALS_PATH and settings.FIREBASE_STORAGE_BUCKET)

if USE_FIREBASE:
    import firebase_admin
    from firebase_admin import credentials, storage

    _app_initialized = False

    def _get_bucket():
        global _app_initialized
        if not _app_initialized:
            if settings.FIREBASE_CREDENTIALS_PATH:
                cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
                firebase_admin.initialize_app(cred, {
                    "storageBucket": settings.FIREBASE_STORAGE_BUCKET,
                })
            else:
                firebase_admin.initialize_app(options={
                    "storageBucket": settings.FIREBASE_STORAGE_BUCKET,
                })
            _app_initialized = True
        return storage.bucket()

    def upload_audio(file_bytes: bytes, filename: str, content_type: str) -> str:
        bucket = _get_bucket()
        blob = bucket.blob(f"audio/{filename}")
        blob.upload_from_string(file_bytes, content_type=content_type)
        blob.make_public()
        return blob.public_url

    def delete_audio(audio_url: str) -> bool:
        bucket = _get_bucket()
        blob_name = (
            audio_url.split(f"{settings.FIREBASE_STORAGE_BUCKET}/")[-1]
            if settings.FIREBASE_STORAGE_BUCKET in audio_url
            else f"audio/{audio_url.split('/')[-1]}"
        )
        blob = bucket.blob(blob_name)
        if blob.exists():
            blob.delete()
            return True
        return False

    def list_all_audio_files() -> list[dict]:
        bucket = _get_bucket()
        blobs = bucket.list_blobs(prefix="audio/")
        return [
            {"name": blob.name, "public_url": blob.public_url}
            for blob in blobs
            if not blob.name.endswith("/")
        ]
else:
    def upload_audio(file_bytes: bytes, filename: str, content_type: str) -> str:
        return store_audio_local(file_bytes, filename)

    def delete_audio(audio_url: str) -> bool:
        return delete_audio_local(audio_url)

    def list_all_audio_files() -> list[dict]:
        return list_all_local_audio()
