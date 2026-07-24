import uuid

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models import RawPhrase
from app.services.firebase import delete_audio, upload_audio


def upload_audio_and_create_phrase(
    file: UploadFile,
    phrase_text: str,
    language: str,
    user_id: int,
    db: Session,
) -> RawPhrase:
    ext = file.filename.rsplit(".", 1)[-1] if file.filename else "webm"
    filename = f"{user_id}_{uuid.uuid4().hex}.{ext}"
    file_bytes = file.file.read()

    try:
        audio_url = upload_audio(file_bytes, filename, file.content_type or "audio/webm")
    except Exception:
        raise

    raw_phrase = RawPhrase(
        language=language,
        phrase=phrase_text,
        audio_url=audio_url,
        submitted_by=user_id,
        status="submitted",
    )
    db.add(raw_phrase)

    try:
        db.commit()
        db.refresh(raw_phrase)
    except Exception:
        db.rollback()
        try:
            delete_audio(audio_url)
        except Exception:
            pass
        raise

    return raw_phrase
