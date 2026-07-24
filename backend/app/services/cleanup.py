from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models import RawPhrase
from app.services.firebase import delete_audio, list_all_audio_files


def cleanup_orphaned_audio(db: Session | None = None) -> dict:
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True

    try:
        db_urls = set(
            row[0] for row in
            db.query(RawPhrase.audio_url)
            .filter(RawPhrase.audio_url.isnot(None))
            .all()
        )

        all_files = list_all_audio_files()
        deleted = 0
        errors = 0

        for af in all_files:
            url = af.get("public_url") or af.get("path") or af.get("name", "")
            if url not in db_urls:
                try:
                    delete_audio(url)
                    deleted += 1
                except Exception:
                    errors += 1

        return {
            "orphans_found": len(all_files) - len(db_urls),
            "deleted": deleted,
            "errors": errors,
        }
    finally:
        if close_db:
            db.close()
