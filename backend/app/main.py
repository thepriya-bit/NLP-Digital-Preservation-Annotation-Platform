from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.db.database import Base, engine, get_db
from app.models import Annotation, RawPhrase, User, Verification
from app.qa.rule_engine import QARuleEngine
from app.schemas import AnnotationCreate, AnnotationRead, RawPhraseCreate, RawPhraseRead

app = FastAPI(title="NLP Platform", version="1.0.0")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "Assamese NLP Platform API is running"}


@app.post("/raw-phrases", response_model=RawPhraseRead)
def create_raw_phrase(payload: RawPhraseCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == payload.submitted_by).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    qa_result = QARuleEngine.validate(payload.phrase, payload.language)
    if not qa_result.is_valid:
        raise HTTPException(status_code=422, detail=qa_result.model_dump())

    raw_phrase = RawPhrase(
        language=payload.language,
        phrase=payload.phrase,
        audio_url=payload.audio_url,
        submitted_by=payload.submitted_by,
        status=payload.status,
    )
    db.add(raw_phrase)
    db.commit()
    db.refresh(raw_phrase)
    return raw_phrase


@app.post("/annotations", response_model=AnnotationRead)
def create_annotation(payload: AnnotationCreate, db: Session = Depends(get_db)):
    raw_phrase = db.query(RawPhrase).filter(RawPhrase.id == payload.raw_phrase_id).first()
    if not raw_phrase:
        raise HTTPException(status_code=404, detail="Raw phrase not found")

    user = db.query(User).filter(User.id == payload.created_by).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    qa_result = QARuleEngine.validate(payload.translated_text, raw_phrase.language)
    if not qa_result.is_valid:
        raise HTTPException(status_code=422, detail=qa_result.model_dump())

    annotation = Annotation(
        raw_phrase_id=payload.raw_phrase_id,
        translated_text=payload.translated_text,
        pos_tags=payload.pos_tags,
        named_entities=payload.named_entities,
        syntax=payload.syntax,
        created_by=payload.created_by,
    )
    db.add(annotation)
    db.commit()
    db.refresh(annotation)
    return annotation


Base.metadata.create_all(bind=engine)
