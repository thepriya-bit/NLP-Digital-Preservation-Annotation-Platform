from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RawPhraseCreate(BaseModel):
    language: str = "assamese"
    phrase: str
    audio_url: str | None = None
    submitted_by: int | None = None
    status: str = "submitted"


class RawPhraseUpdate(BaseModel):
    language: str | None = None
    phrase: str | None = None
    audio_url: str | None = None
    status: str | None = None


class RawPhraseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    language: str
    phrase: str
    audio_url: str | None = None
    submitted_by: int
    status: str
    created_at: datetime
