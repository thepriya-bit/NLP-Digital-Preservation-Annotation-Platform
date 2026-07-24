from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin
from app.db.database import get_db
from app.models import Annotation, RawPhrase, User, Verification
from app.schemas import UserAdminUpdate, UserRead
from app.services.cleanup import cleanup_orphaned_audio
from app.services.export_service import export_stats

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users", response_model=list[UserRead])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return db.query(User).order_by(User.id).all()


@router.get("/users/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/users/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    payload: UserAdminUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


@router.post("/users/{user_id}/ban")
def ban_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot ban yourself")
    user.is_banned = True
    db.commit()
    return {"message": f"User '{user.username}' has been banned"}


@router.post("/users/{user_id}/unban")
def unban_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_banned = False
    db.commit()
    return {"message": f"User '{user.username}' has been unbanned"}


@router.get("/stats")
def get_platform_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    total_users = db.query(User).count()
    total_phrases = db.query(RawPhrase).count()
    export_data = export_stats(db)
    return {
        "total_users": total_users,
        "total_phrases": total_phrases,
        **export_data,
    }


@router.post("/cleanup/orphans")
def trigger_orphan_cleanup(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    result = cleanup_orphaned_audio(db)
    return result


@router.get("/dashboard")
def admin_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    recent_users = (
        db.query(User).order_by(User.created_at.desc()).limit(5).all()
    )
    recent_annotations = (
        db.query(Annotation).order_by(Annotation.created_at.desc()).limit(5).all()
    )
    return {
        "recent_users": [
            {"id": u.id, "username": u.username, "role": u.role, "trust_score": u.trust_score, "is_banned": u.is_banned}
            for u in recent_users
        ],
        "recent_annotations": [
            {"id": a.id, "translated_text": a.translated_text[:100], "created_by": a.created_by}
            for a in recent_annotations
        ],
    }
