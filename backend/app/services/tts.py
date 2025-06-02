from transformers import AutoTokenizer, AutoModelForTextToWaveform
import torch
import scipy.io.wavfile as wavfile
import io
from fastapi import HTTPException
from huggingface_hub import login
import logging

logger = logging.getLogger(__name__)

class TTSService:
    def __init__(self):
        try:
            # Initialize with your Hugging Face token
            login("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")
            
            self.tokenizer = AutoTokenizer.from_pretrained("CMawuena/farmerline-akan-tts")
            self.model = AutoModelForTextToWaveform.from_pretrained("CMawuena/farmerline-akan-tts")
            self.sample_rate = getattr(self.model.config, "sampling_rate", 22050)
        except Exception as e:
            logger.error(f"TTS model loading failed: {str(e)}")
            raise RuntimeError("Could not initialize TTS service")

    def generate_audio(self, text: str) -> io.BytesIO:
        """Generate audio from text and return in-memory WAV file"""
        try:
            inputs = self.tokenizer(text, return_tensors="pt")
            
            with torch.no_grad():
                waveform = self.model(**inputs).waveform
            
            audio = waveform.squeeze().cpu().numpy()
            
            # Create in-memory WAV file
            buffer = io.BytesIO()
            wavfile.write(buffer, self.sample_rate, audio)
            buffer.seek(0)
            
            return buffer
        except Exception as e:
            logger.error(f"Audio generation failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Audio generation failed")
