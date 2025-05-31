from fastapi import APIRouter, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.services.ocr import OCRService
from app.models.job import ProcessingJob
from app.schemas.job import JobCreate
from app.core.config import get_db
from pathlib import Path
import tempfile
import os


router = APIRouter(prefix="", tags=["ocr"])  # prefix="" because we set it in main.py

from ....schemas.ocr import OCRResult


@router.post("/", response_model=OCRResult)
async def extract_text_from_image(
        image_file: UploadFile,
        db: Session = Depends(get_db)
):
    try:
        # Validate file type
        allowed_extensions = {'.jpg', '.jpeg', '.png'}
        file_ext = Path(image_file.filename).suffix.lower()
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed types: {', '.join(allowed_extensions)}"
            )

        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix=file_ext, delete=False) as tmp:
            contents = await image_file.read()
            tmp.write(contents)
            tmp_path = tmp.name

        # Process image
        service = OCRService()
        result = service.extract_text(tmp_path)  # This now returns OCRResult format

        # Clean up
        os.unlink(tmp_path)

        # Save to database
        job = JobCreate(
            job_type="ocr",
            input_file=image_file.filename,
            status="completed",
            result=result.text  # Access as attribute now
        )

        db_job = ProcessingJob(**job.dict())
        db.add(db_job)
        db.commit()
        db.refresh(db_job)

        # Return OCRResult directly
        return result

    except Exception as e:
        if 'tmp_path' in locals():
            try:
                os.unlink(tmp_path)
            except:
                pass
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))