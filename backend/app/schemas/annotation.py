from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class AnnotationCreate(BaseModel):
    raw_phrase_id: int
    translated_text: str
    pos_tags: dict[str, Any] | None = None
    named_entities: dict[str, Any] | None = None
    syntax: dict[str, Any] | None = None
    created_by: int | None = None


class AnnotationUpdate(BaseModel):
    translated_text: str | None = None
    pos_tags: dict[str, Any] | None = None
    named_entities: dict[str, Any] | None = None
    syntax: dict[str, Any] | None = None


class AnnotationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    raw_phrase_id: int
    translated_text: str
    pos_tags: dict[str, Any] | None = None
    named_entities: dict[str, Any] | None = None
    syntax: dict[str, Any] | None = None
    created_by: int
    created_at: datetime


class SyntaxTagRequest(BaseModel):
    text: str
    language: str = "assamese"


class SyntaxTagResponse(BaseModel):
    tokens: list[str]
    pos_tags: list[dict[str, str]]
    named_entities: list[dict[str, str]]
    syntax_tree: dict[str, Any] | None = None
