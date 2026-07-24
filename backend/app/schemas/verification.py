from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, field_validator


class VoteEnum(str, Enum):
    APPROVE = "approve"
    REJECT = "reject"


class VerificationCreate(BaseModel):
    annotation_id: int
    vote: VoteEnum
    comment: str | None = None


class VerificationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    annotation_id: int
    verifier_id: int
    vote: str
    comment: str | None = None
    created_at: datetime


class VerificationResult(BaseModel):
    success: bool
    verification: VerificationRead | None = None
    annotation_status: str | None = None
    error: str | None = None


class PendingAnnotation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    raw_phrase_id: int
    translated_text: str
    created_by: int
    created_at: datetime
    approve_count: int = 0
    reject_count: int = 0
