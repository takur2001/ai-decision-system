from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.services.file_reader import FileReaderService
from app.services.ai_processor import AIProcessor
from app.services.llm_service import LLMService
from app.services.decision_engine import DecisionEngine
from app.models.database import SessionLocal
from app.models.case import Case
from app.core.security import get_current_user

router = APIRouter()

UPLOAD_DIR = Path("data/raw")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_case(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="File must have a name")

    file_path = UPLOAD_DIR / file.filename

    try:
        contents = await file.read()

        with open(file_path, "wb") as f:
            f.write(contents)

        extracted_text = FileReaderService.extract_text(file_path)
        entities = AIProcessor.extract_entities(extracted_text)
        summary = AIProcessor.summarize(extracted_text)
        llm_result = LLMService.analyze(extracted_text)
        fallback_decision = DecisionEngine.generate_decision(entities)

        db = SessionLocal()
        try:
            new_case = Case(
                filename=file.filename,
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
        finally:
            db.close()

        return {
            "message": "File uploaded and fully analyzed",
            "filename": file.filename,
            "file_type": file_path.suffix,
            "characters_extracted": len(extracted_text),
            "summary": summary,
            "entities": entities,
            "llm_status": llm_result["status"],
            "llm_analysis": llm_result["analysis"],
            "fallback_decision": fallback_decision,
            "case_id": new_case.id,
            "user": {
                "user_id": current_user["user_id"],
                "email": current_user["sub"]
            },
            "preview": extracted_text[:500]
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))