from typing import Optional
from ..schemas.translation import TranslationResult
from deep_translator import GoogleTranslator

class TranslationService:
    async def translate_text(
        self,
        text: str,
        target_language: str = "en",
        source_language: Optional[str] = None
    ) -> TranslationResult:
        try:
            translated = GoogleTranslator(
                source=source_language or 'auto',
                target=target_language
            ).translate(text)
            
            return TranslationResult(
                original_text=text,
                translated_text=translated,
                source_language=source_language or "auto",
                target_language=target_language,
                confidence=None  # deep-translator doesn't provide confidence
            )
        except Exception as e:
            raise ValueError(f"Translation failed: {str(e)}")
