from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import Annotation, User, Verification


def _update_trust_score(db: Session, user_id: int, approved: bool) -> None:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return

    if approved:
        user.trust_score = min(
            user.trust_score + settings.TRUST_SCORE_INCREMENT,
            settings.TRUST_SCORE_MAX,
        )
    else:
        user.trust_score = max(
            user.trust_score - settings.TRUST_SCORE_PENALTY,
            settings.TRUST_SCORE_MIN,
        )
    db.commit()


def _check_consensus(db: Session, annotation_id: int) -> str | None:
    annotation = db.query(Annotation).filter(Annotation.id == annotation_id).first()
    if not annotation:
        return None

    approve_count = (
        db.query(Verification)
        .filter(
            Verification.annotation_id == annotation_id,
            Verification.vote == "approve",
        )
        .count()
    )
    reject_count = (
        db.query(Verification)
        .filter(
            Verification.annotation_id == annotation_id,
            Verification.vote == "reject",
        )
        .count()
    )

    if approve_count >= settings.VERIFICATION_APPROVAL_THRESHOLD:
        annotation.syntax = annotation.syntax or {}
        annotation.syntax["verification_status"] = "verified"
        db.commit()
        _update_trust_score(db, annotation.created_by, approved=True)
        return "verified"

    if reject_count >= settings.VERIFICATION_REJECTION_THRESHOLD:
        annotation.syntax = annotation.syntax or {}
        annotation.syntax["verification_status"] = "rejected"
        db.commit()
        _update_trust_score(db, annotation.created_by, approved=False)
        return "rejected"

    return None


def cast_vote(
    db: Session,
    annotation_id: int,
    verifier_id: int,
    vote: str,
    comment: str | None = None,
) -> dict:
    annotation = db.query(Annotation).filter(Annotation.id == annotation_id).first()
    if not annotation:
        return {"success": False, "error": "Annotation not found"}

    if annotation.created_by == verifier_id:
        return {"success": False, "error": "Cannot vote on your own annotation"}

    existing = (
        db.query(Verification)
        .filter(
            Verification.annotation_id == annotation_id,
            Verification.verifier_id == verifier_id,
        )
        .first()
    )
    if existing:
        return {"success": False, "error": "You have already voted on this annotation"}

    verification = Verification(
        annotation_id=annotation_id,
        verifier_id=verifier_id,
        vote=vote,
        comment=comment,
    )
    db.add(verification)
    db.commit()
    db.refresh(verification)

    status = _check_consensus(db, annotation_id)

    return {
        "success": True,
        "verification": verification,
        "annotation_status": status,
    }


def get_pending_annotations(
    db: Session,
    skip: int = 0,
    limit: int = 20,
) -> list[Annotation]:
    return (
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


def get_votes_for_annotation(db: Session, annotation_id: int) -> list[Verification]:
    return (
        db.query(Verification)
        .filter(Verification.annotation_id == annotation_id)
        .all()
    )


def get_my_votes(
    db: Session,
    verifier_id: int,
    skip: int = 0,
    limit: int = 20,
) -> list[Verification]:
    return (
        db.query(Verification)
        .filter(Verification.verifier_id == verifier_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
