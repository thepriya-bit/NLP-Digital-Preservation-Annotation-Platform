import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "NLP Platform")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:password@localhost:5432/nlp_platform",
    )
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")
    FIREBASE_CREDENTIALS_PATH: str = os.getenv("FIREBASE_CREDENTIALS_PATH", "")
    FIREBASE_STORAGE_BUCKET: str = os.getenv("FIREBASE_STORAGE_BUCKET", "")
    LOCAL_AUDIO_DIR: str = os.getenv("LOCAL_AUDIO_DIR", "uploads/audio")

    VERIFICATION_APPROVAL_THRESHOLD: int = int(os.getenv("VERIFICATION_APPROVAL_THRESHOLD", "2"))
    VERIFICATION_REJECTION_THRESHOLD: int = int(os.getenv("VERIFICATION_REJECTION_THRESHOLD", "2"))
    TRUST_SCORE_INCREMENT: float = float(os.getenv("TRUST_SCORE_INCREMENT", "1.0"))
    TRUST_SCORE_PENALTY: float = float(os.getenv("TRUST_SCORE_PENALTY", "2.0"))
    TRUST_SCORE_MIN: float = float(os.getenv("TRUST_SCORE_MIN", "-100.0"))
    TRUST_SCORE_MAX: float = float(os.getenv("TRUST_SCORE_MAX", "100.0"))


settings = Settings()
