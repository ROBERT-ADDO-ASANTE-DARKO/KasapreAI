from fastapi import APIRouter
from .endpoints import transcription

router = APIRouter(prefix="/api/v1")

router.include_router(
    transcription.router,
    prefix="/transcription",
    tags=["transcription"]
)

# Include other routers here as you create them
# from .endpoints import ocr, translation
# router.include_router(ocr.router, prefix="/ocr", tags=["ocr"])
# router.include_router(translation.router, prefix="/translation", tags=["translation"])