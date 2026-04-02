from fastapi import APIRouter, Depends
from app.models.database import SessionLocal
from app.models.case import Case
from app.core.security import get_current_user

router = APIRouter()


@router.get("/history")
def get_case_history(current_user=Depends(get_current_user)):
    db = SessionLocal()
    try:
        cases = (
            db.query(Case)
            .filter(Case.user_id == current_user["user_id"])
            .order_by(Case.id.desc())
            .all()
        )

        return [
            {
                "id": case.id,
                "filename": case.filename,
                "summary": case.summary,
                "amount": case.amount,
                "date": case.date,
                "issue_type": case.issue_type,
                "risk_level": case.risk_level,
                "risk_score": case.risk_score,
                "confidence_score": case.confidence_score,
                "decision": case.decision,
                "user_id": case.user_id,
            }
            for case in cases
        ]
    finally:
        db.close()