from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_admin
from app.db.database import get_db
from app.models import Annotation, RawPhrase, User
from app.qa.rule_engine import QARuleEngine
from app.schemas import AnnotationCreate, AnnotationRead, AnnotationUpdate

router = APIRouter(prefix="/annotations", tags=["Annotations"])


@router.get("", response_model=list[AnnotationRead])
def list_annotations(
    raw_phrase_id: int | None = Query(None),
    created_by: int | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Annotation)
    if raw_phrase_id is not None:
        query = query.filter(Annotation.raw_phrase_id == raw_phrase_id)
    if created_by is not None:
        query = query.filter(Annotation.created_by == created_by)
    return query.offset(skip).limit(limit).all()


@router.get("/my", response_model=list[AnnotationRead])
def my_annotations(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Annotation)
        .filter(Annotation.created_by == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.post("", response_model=AnnotationRead, status_code=status.HTTP_201_CREATED)
def create_annotation(
    payload: AnnotationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    raw_phrase = db.query(RawPhrase).filter(RawPhrase.id == payload.raw_phrase_id).first()
    if not raw_phrase:
        raise HTTPException(status_code=404, detail="Raw phrase not found")

    qa_result = QARuleEngine.validate(payload.translated_text, "english")
    if not qa_result.is_valid:
        raise HTTPException(status_code=422, detail="; ".join(e.message for e in qa_result.errors))

    annotation = Annotation(
        raw_phrase_id=payload.raw_phrase_id,
        translated_text=payload.translated_text,
        pos_tags=payload.pos_tags,
        named_entities=payload.named_entities,
        syntax=payload.syntax,
        created_by=current_user.id,
    )
    db.add(annotation)
    db.commit()
    db.refresh(annotation)
    return annotation


@router.get("/{annotation_id}", response_model=AnnotationRead)
def get_annotation(annotation_id: int, db: Session = Depends(get_db)):
    annotation = db.query(Annotation).filter(Annotation.id == annotation_id).first()
    if not annotation:
        raise HTTPException(status_code=404, detail="Annotation not found")
    return annotation


@router.put("/{annotation_id}", response_model=AnnotationRead)
def update_annotation(
    annotation_id: int,
    payload: AnnotationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    annotation = db.query(Annotation).filter(Annotation.id == annotation_id).first()
    if not annotation:
        raise HTTPException(status_code=404, detail="Annotation not found")
    if annotation.created_by != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this annotation",
        )

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(annotation, field, value)

    db.commit()
    db.refresh(annotation)
    return annotation


@router.delete("/{annotation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_annotation(
    annotation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    annotation = db.query(Annotation).filter(Annotation.id == annotation_id).first()
    if not annotation:
        raise HTTPException(status_code=404, detail="Annotation not found")
    if annotation.created_by != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this annotation",
        )
    db.delete(annotation)
    db.commit()
