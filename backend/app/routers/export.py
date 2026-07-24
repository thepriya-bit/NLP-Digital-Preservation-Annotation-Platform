from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session

from app.core.dependencies import require_verifier
from app.db.database import get_db
from app.models import User
from app.services.export_service import export_csv, export_json, export_parquet, export_stats

router = APIRouter(prefix="/export", tags=["Export"])


@router.get("/csv")
def download_csv(
    language: str | None = Query(None),
    date_from: date | None = Query(None),
    date_to: date | None = Query(None),
    min_trust_score: float | None = Query(None, ge=-100, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_verifier),
):
    content = export_csv(db, language, date_from, date_to, min_trust_score)
    return Response(
        content=content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=verified_dataset.csv"},
    )


@router.get("/json")
def download_json(
    language: str | None = Query(None),
    date_from: date | None = Query(None),
    date_to: date | None = Query(None),
    min_trust_score: float | None = Query(None, ge=-100, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_verifier),
):
    content = export_json(db, language, date_from, date_to, min_trust_score)
    return Response(
        content=content,
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=verified_dataset.json"},
    )


@router.get("/parquet")
def download_parquet(
    language: str | None = Query(None),
    date_from: date | None = Query(None),
    date_to: date | None = Query(None),
    min_trust_score: float | None = Query(None, ge=-100, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_verifier),
):
    try:
        content = export_parquet(db, language, date_from, date_to, min_trust_score)
    except ImportError:
        raise HTTPException(
            status_code=501,
            detail="Parquet export requires pyarrow. Install with: pip install pyarrow",
        )
    return Response(
        content=content,
        media_type="application/octet-stream",
        headers={"Content-Disposition": "attachment; filename=verified_dataset.parquet"},
    )


@router.get("/stats")
def get_export_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_verifier),
):
    return export_stats(db)
