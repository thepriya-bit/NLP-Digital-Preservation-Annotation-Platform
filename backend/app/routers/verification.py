from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_verifier
from app.db.database import get_db
from app.models import Annotation, User, Verification
from app.schemas import VerificationCreate, VerificationRead, VerificationResult
from app.schemas.verification import PendingAnnotation, VoteEnum
from app.services.verification_service import cast_vote, get_votes_for_annotation

router = APIRouter(prefix="/verifications", tags=["Verifications"])


@router.post("", response_model=VerificationResult, status_code=status.HTTP_201_CREATED)
def create_verification(
    payload: VerificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_verifier),
):
    result = cast_vote(
        db=db,
        annotation_id=payload.annotation_id,
        verifier_id=current_user.id,
        vote=payload.vote.value,
        comment=payload.comment,
    )
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=result["error"])
    return VerificationResult(
        success=True,
        verification=result["verification"],
        annotation_status=result.get("annotation_status"),
    )


@router.get("/pending", response_model=list[PendingAnnotation])
def list_pending_annotations(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_verifier),
):
    annotations = (
        db.query(Annotation)
        .filter(
            Annotation.syntax.is_(None)
            | Annotation.syntax["verification_status"].astext.is_(None)
        )
        .order_by(Annotation.created_at.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    result = []
    for a in annotations:
        approve_count = (
            db.query(Verification)
            .filter(Verification.annotation_id == a.id, Verification.vote == "approve")
            .count()
        )
        reject_count = (
            db.query(Verification)
            .filter(Verification.annotation_id == a.id, Verification.vote == "reject")
            .count()
        )
        result.append(
            PendingAnnotation(
                id=a.id,
                raw_phrase_id=a.raw_phrase_id,
                translated_text=a.translated_text,
                created_by=a.created_by,
                created_at=a.created_at,
                approve_count=approve_count,
                reject_count=reject_count,
            )
        )
    return result


@router.get("/my", response_model=list[VerificationRead])
def my_verifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_verifier),
):
    return (
        db.query(Verification)
        .filter(Verification.verifier_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/{annotation_id}", response_model=list[VerificationRead])
def get_annotation_votes(
    annotation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_verifier),
):
    annotation = db.query(Annotation).filter(Annotation.id == annotation_id).first()
    if not annotation:
        raise HTTPException(status_code=404, detail="Annotation not found")
    return get_votes_for_annotation(db, annotation_id)
