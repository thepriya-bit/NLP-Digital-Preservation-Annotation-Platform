from typing import Any
from pydantic import BaseModel, ConfigDict


class AnnotationCreate(BaseModel):
    raw_phrase_id: int
    translated_text: str
    pos_tags: dict[str, Any] | None = None
    named_entities: dict[str, Any] | None = None
    syntax: dict[str, Any] | None = None
    created_by: int


class AnnotationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    raw_phrase_id: int
    translated_text: str
    pos_tags: dict[str, Any] | None = None
    named_entities: dict[str, Any] | None = None
    syntax: dict[str, Any] | None = None
    created_by: int
