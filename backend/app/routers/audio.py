import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status

from app.core.dependencies import get_current_user
from app.models import User
from app.services.firebase import upload_audio

router = APIRouter(prefix="/audio", tags=["Audio"])

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
ALLOWED_CONTENT_TYPES = [
    "audio/webm",
    "audio/mp3",
    "audio/mpeg",
    "audio/wav",
    "audio/ogg",
    "audio/x-wav",
    "audio/x-m4a",
    "audio/mp4",
    "audio/aac",
]


@router.post("/upload")
def upload_audio_file(
    file: UploadFile,
    current_user: User = Depends(get_current_user),
):
    if not file.content_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not detect file type. Ensure the file has a valid audio format.",
        )

    if file.content_type not in ALLOWED_CONTENT_TYPES and not file.content_type.startswith("audio/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File must be an audio type. Got: {file.content_type}",
        )

    ext = file.filename.rsplit(".", 1)[-1] if file.filename else "webm"
    filename = f"{current_user.id}_{uuid.uuid4().hex}.{ext}"
    file_bytes = file.file.read()

    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)} MB.",
        )

    audio_url = upload_audio(file_bytes, filename, file.content_type)
    return {"audio_url": audio_url, "filename": filename}
