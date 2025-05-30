from pydantic import BaseModel
from typing import Optional

class TranslationRequest(BaseModel):
    text: str
    target_language: str = "en"  # Default to English
    source_language: Optional[str] = None  # Auto-detect if None

class TranslationResult(BaseModel):
    original_text: str
    translated_text: str
    source_language: str  # No longer optional in response
    target_language: str
    confidence: Optional[float] = None
