from .transcription import router as transcription_router
from .ocr import router as ocr_router
from .translation import router as translation_router
from .tts import router as tts_router

__all__ = [
    "transcription_router", 
    "ocr_router",
    "translation_router",
    "tts_router"
]
