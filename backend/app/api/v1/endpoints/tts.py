from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from ....services.tts import TTSService
from ....schemas.tts import TTSRequest, TTSResponse
from app.models.job import ProcessingJob
from app.schemas.job import JobCreate
from app.core.config import get_db
from typing import Optional

router = APIRouter()

@router.post("/", response_model=TTSResponse)
async def text_to_speech(
    request: TTSRequest,
    db: Session = Depends(get_db)
):
    try:
        service = TTSService()
        audio_buffer = service.generate_audio(request.text)
        
        # Save to database
        job = JobCreate(
            job_type="tts",
            input_file=None,
            status="completed",
            result=f"Generated {len(request.text)} characters"
        )
        
        db_job = ProcessingJob(**job.model_dump())
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        
        return StreamingResponse(
            audio_buffer,
            media_type="audio/wav",
            headers={
                "Content-Disposition": "attachment; filename=speech.wav",
                "Text-Length": str(len(request.text)),
                "Sample-Rate": str(service.sample_rate)
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
