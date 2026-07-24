from app.db.database import SessionLocal
from app.services.cleanup import cleanup_orphaned_audio

if __name__ == "__main__":
    db = SessionLocal()
    try:
        result = cleanup_orphaned_audio(db)
        print("Cleanup result:", result)
    finally:
        db.close()
