from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from .api.v1.router import router as api_router
from app.api.v1.endpoints import transcription, ocr, translation

app = FastAPI(generate_unique_id_function=lambda route: f"{route.tags[0]}_{route.name}")

app.include_router(api_router)

#app = FastAPI(
#    title="Polyglot API",
#    description="Multilingual Communication Suite",
#    version="1.0.0"
#)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#app.include_router(api_router, prefix="/api/v1")
app.include_router(
    transcription.router,
    prefix="/api/v1/transcription",
    tags=["Audio Transcription"]
)

app.include_router(
    ocr.router,
    prefix="/api/v1/ocr",
    tags=["Image OCR"]
)

app.include_router(
    translation.router,
    prefix="/api/v1/translation",
    tags=["Text Translation"]
)
