import whisper
from tempfile import NamedTemporaryFile
from ..core.config import settings
from ..models.job import ProcessingJob
from ..schemas.job import Job

class TranscriptionService:
    def __init__(self):
        self.model = whisper.load_model("base")
    
    def transcribe_audio(self, file_path: str) -> str:
        """Sync method since Whisper is synchronous"""
        result = self.model.transcribe(file_path)
        return result['text']
