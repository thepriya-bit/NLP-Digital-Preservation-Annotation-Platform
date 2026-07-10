from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Annotation(Base):
    __tablename__ = "annotations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    raw_phrase_id: Mapped[int] = mapped_column(ForeignKey("raw_phrases.id"), nullable=False)
    translated_text: Mapped[str] = mapped_column(Text, nullable=False)
    pos_tags: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    named_entities: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    syntax: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    raw_phrase: Mapped["RawPhrase"] = relationship(back_populates="annotations")
    created_by_user: Mapped["User"] = relationship(back_populates="annotations")
    verifications: Mapped[list["Verification"]] = relationship(back_populates="annotation")
