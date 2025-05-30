from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ....services.translation import TranslationService
from ....schemas.translation import TranslationRequest, TranslationResult
from ....models.job import ProcessingJob
from ....schemas.job import JobCreate
from ....core.config import get_db

router = APIRouter()

@router.post("/", response_model=TranslationResult)
async def translate_text(
    request: TranslationRequest,
    db: Session = Depends(get_db)
):
    try:
        service = TranslationService()
        result = await service.translate_text(
            text=request.text,
            target_language=request.target_language,
            source_language=request.source_language
        )
        
        # Save to database
        job = JobCreate(
            job_type="translation",
            input_file=None,
            status="completed",
            result=result.model_dump_json()
        )
        
        db_job = ProcessingJob(**job.model_dump())
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
