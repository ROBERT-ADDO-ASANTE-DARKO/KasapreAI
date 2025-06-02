from pydantic import BaseModel

class TTSRequest(BaseModel):
    text: str
    language: str = "ak"  # Akan language code

class TTSResponse(BaseModel):
    audio_format: str = "audio/wav"
    text_length: int
    sample_rate: int
