from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.services.ai_processor import AIProcessor
from app.services.llm_service import LLMService
from app.services.decision_engine import DecisionEngine
from app.models.database import SessionLocal
from app.models.case import Case
from app.core.security import get_current_user

router = APIRouter()


class TextRequest(BaseModel):
    text: str


@router.post("/analyze-text")
def analyze_text(request: TextRequest, current_user=Depends(get_current_user)):
    text = request.text

    entities = AIProcessor.extract_entities(text)
    summary = AIProcessor.summarize(text)
    llm_result = LLMService.analyze(text)
    fallback_decision = DecisionEngine.generate_decision(entities)

    db = SessionLocal()
    try:
        new_case = Case(
            filename="text_input",
            summary=summary,
            amount=entities.get("amount"),
            date=entities.get("date"),
            issue_type=entities.get("issue_type"),
            risk_level=entities.get("risk_level"),
            risk_score=fallback_decision.get("risk_score"),
            confidence_score=fallback_decision.get("confidence_score"),
            decision=fallback_decision.get("recommended_action"),
            user_id=current_user["user_id"]
        )

        db.add(new_case)
        db.commit()
        db.refresh(new_case)

        return {
            "message": "Text analyzed successfully",
            "summary": summary,
            "entities": entities,
            "llm_status": llm_result["status"],
            "llm_analysis": llm_result["analysis"],
            "fallback_decision": fallback_decision,
            "case_id": new_case.id,
            "user": {
                "user_id": current_user["user_id"],
                "email": current_user["sub"]
            }
        }
    finally:
        db.close()