from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict


class VerificationCreate(BaseModel):
    annotation_id: int
    verifier_id: int
    vote: str
    comment: str | None = None


class VerificationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    annotation_id: int
    verifier_id: int
    vote: str
    comment: str | None = None
    created_at: datetime
