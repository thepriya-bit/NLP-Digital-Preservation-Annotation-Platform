from pydantic import BaseModel, ConfigDict


class RawPhraseCreate(BaseModel):
    language: str = "assamese"
    phrase: str
    audio_url: str | None = None
    submitted_by: int
    status: str = "submitted"


class RawPhraseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    language: str
    phrase: str
    audio_url: str | None = None
    submitted_by: int
    status: str
