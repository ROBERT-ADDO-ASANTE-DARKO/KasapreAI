from fastapi import APIRouter, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pathlib import Path
import os
from ....services.transcription import TranscriptionService
from ....models.job import ProcessingJob
from ....schemas.job import JobCreate
from ....dependencies import get_db
import tempfile

router = APIRouter(prefix="", tags=["transcription"])  # prefix="" because we set it in main.py


@router.post("/", response_model=dict)
async def transcribe_audio(
        audio_file: UploadFile,
        db: Session = Depends(get_db)
):
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            # Read uploaded file content and write to temp file
            contents = await audio_file.read()
            tmp.write(contents)
            tmp_path = tmp.name

        # Pass file path to service
        service = TranscriptionService()
        transcription = service.transcribe_audio(tmp_path)  # Remove await since we're using sync Whisper

        # Clean up
        os.unlink(tmp_path)

        # Save to database
        job = JobCreate(
            job_type="transcription",
            input_file=audio_file.filename,
            status="completed",
            result=transcription
        )

        db_job = ProcessingJob(**job.dict())
        db.add(db_job)
        db.commit()
        db.refresh(db_job)

        return {
            "status": "success",
            "job_id": db_job.id,
            "transcription": transcription
        }
    except Exception as e:
        if 'tmp_path' in locals():
            try:
                os.unlink(tmp_path)
            except:
                pass
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))