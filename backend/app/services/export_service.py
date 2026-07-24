import csv
import io
import json
from datetime import date, datetime

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.models import Annotation, RawPhrase, User, Verification


def _get_verified_annotations(
    db: Session,
    language: str | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    min_trust_score: float | None = None,
):
    query = (
        db.query(Annotation)
        .join(RawPhrase)
        .join(User, Annotation.created_by == User.id)
        .options(joinedload(Annotation.raw_phrase), joinedload(Annotation.created_by_user))
        .filter(
            Annotation.syntax.isnot(None),
            Annotation.syntax["verification_status"].astext == "verified",
        )
    )

    if language:
        query = query.filter(RawPhrase.language == language)
    if date_from:
        query = query.filter(Annotation.created_at >= datetime.combine(date_from, datetime.min.time()))
    if date_to:
        query = query.filter(Annotation.created_at <= datetime.combine(date_to, datetime.max.time()))
    if min_trust_score is not None:
        query = query.filter(User.trust_score >= min_trust_score)

    return query.order_by(Annotation.created_at.asc()).all()


def _build_rows(annotations: list[Annotation]) -> list[dict]:
    rows = []
    for a in annotations:
        rp = a.raw_phrase
        user = a.created_by_user
        rows.append({
            "annotation_id": a.id,
            "phrase_id": rp.id,
            "language": rp.language,
            "phrase": rp.phrase,
            "translated_text": a.translated_text,
            "pos_tags": json.dumps(a.pos_tags, ensure_ascii=False) if a.pos_tags else "",
            "named_entities": json.dumps(a.named_entities, ensure_ascii=False) if a.named_entities else "",
            "syntax": json.dumps(a.syntax, ensure_ascii=False) if a.syntax else "",
            "contributor_username": user.username if user else "",
            "contributor_trust_score": user.trust_score if user else 0.0,
            "verified_at": a.created_at.isoformat() if a.created_at else "",
        })
    return rows


def export_csv(
    db: Session,
    language: str | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    min_trust_score: float | None = None,
) -> str:
    annotations = _get_verified_annotations(db, language, date_from, date_to, min_trust_score)
    rows = _build_rows(annotations)

    output = io.StringIO()
    if rows:
        writer = csv.DictWriter(output, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    return output.getvalue()


def export_json(
    db: Session,
    language: str | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    min_trust_score: float | None = None,
) -> str:
    annotations = _get_verified_annotations(db, language, date_from, date_to, min_trust_score)
    rows = _build_rows(annotations)
    for r in rows:
        r["pos_tags"] = json.loads(r["pos_tags"]) if r["pos_tags"] else None
        r["named_entities"] = json.loads(r["named_entities"]) if r["named_entities"] else None
        r["syntax"] = json.loads(r["syntax"]) if r["syntax"] else None
    return json.dumps(rows, ensure_ascii=False, indent=2)


def export_parquet(
    db: Session,
    language: str | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    min_trust_score: float | None = None,
) -> bytes:
    import pyarrow as pa
    import pyarrow.parquet as pq

    annotations = _get_verified_annotations(db, language, date_from, date_to, min_trust_score)
    rows = _build_rows(annotations)

    table = pa.Table.from_pydict(
        {k: [row[k] for row in rows] for k in (rows[0].keys() if rows else [])}
        if rows
        else {}
    )
    buf = io.BytesIO()
    pq.write_table(table, buf)
    return buf.getvalue()


def export_stats(db: Session) -> dict:
    total_annotations = db.query(Annotation).count()
    verified_count = (
        db.query(Annotation)
        .filter(
            Annotation.syntax.isnot(None),
            Annotation.syntax["verification_status"].astext == "verified",
        )
        .count()
    )
    pending_count = (
        db.query(Annotation)
        .filter(
            Annotation.syntax.is_(None)
            | Annotation.syntax["verification_status"].astext.is_(None),
        )
        .count()
    )

    language_distribution = {}
    for row in db.query(RawPhrase.language, func.count(RawPhrase.id)).group_by(RawPhrase.language).all():
        language_distribution[row[0]] = row[1]

    return {
        "total_annotations": total_annotations,
        "verified_annotations": verified_count,
        "pending_verification": pending_count,
        "language_distribution": language_distribution,
    }
