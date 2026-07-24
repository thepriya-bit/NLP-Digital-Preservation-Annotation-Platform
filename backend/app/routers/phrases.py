from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_admin, require_verifier
from app.db.database import get_db
from app.models import RawPhrase, User
from app.qa.rule_engine import QARuleEngine
from app.schemas import RawPhraseCreate, RawPhraseRead, RawPhraseUpdate

router = APIRouter(prefix="/phrases", tags=["Phrases"])


@router.get("", response_model=list[RawPhraseRead])
def list_phrases(
    status: str | None = Query(None),
    language: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(RawPhrase)
    if status:
        query = query.filter(RawPhrase.status == status)
    if language:
        query = query.filter(RawPhrase.language == language)
    return query.offset(skip).limit(limit).all()


@router.get("/random", response_model=RawPhraseRead)
def get_random_phrase(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    phrase = (
        db.query(RawPhrase)
        .filter(RawPhrase.status == "submitted")
        .order_by(func.random())
        .first()
    )
    if not phrase:
        raise HTTPException(status_code=404, detail="No phrases available for review")
    return phrase


@router.get("/my", response_model=list[RawPhraseRead])
def my_phrases(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(RawPhrase)
        .filter(RawPhrase.submitted_by == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.post("", response_model=RawPhraseRead, status_code=status.HTTP_201_CREATED)
def create_raw_phrase(
    payload: RawPhraseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    qa_result = QARuleEngine.validate(payload.phrase, payload.language)
    if not qa_result.is_valid:
        raise HTTPException(status_code=422, detail="; ".join(e.message for e in qa_result.errors))

    raw_phrase = RawPhrase(
        language=payload.language,
        phrase=payload.phrase,
        audio_url=payload.audio_url,
        submitted_by=current_user.id,
        status=payload.status,
    )
    db.add(raw_phrase)
    db.commit()
    db.refresh(raw_phrase)
    return raw_phrase


@router.get("/{phrase_id}", response_model=RawPhraseRead)
def get_phrase(phrase_id: int, db: Session = Depends(get_db)):
    phrase = db.query(RawPhrase).filter(RawPhrase.id == phrase_id).first()
    if not phrase:
        raise HTTPException(status_code=404, detail="Phrase not found")
    return phrase


@router.put("/{phrase_id}", response_model=RawPhraseRead)
def update_phrase(
    phrase_id: int,
    payload: RawPhraseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_verifier),
):
    phrase = db.query(RawPhrase).filter(RawPhrase.id == phrase_id).first()
    if not phrase:
        raise HTTPException(status_code=404, detail="Phrase not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(phrase, field, value)

    db.commit()
    db.refresh(phrase)
    return phrase


@router.delete("/{phrase_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_phrase(
    phrase_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    phrase = db.query(RawPhrase).filter(RawPhrase.id == phrase_id).first()
    if not phrase:
        raise HTTPException(status_code=404, detail="Phrase not found")
    db.delete(phrase)
    db.commit()
