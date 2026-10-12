"""ASR Component using OpenAI Whisper for real-time speech recognition"""

import whisper
import logging
from .pipeline import BaseASRComponent

logger = logging.getLogger(__name__)


class WhisperASR(BaseASRComponent):
    """Whisper-based ASR for real-time transcription"""
    
    def __init__(self, model_size: str = "base", device: str = "cpu"):
        self.model_size = model_size
        self.device = device
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load Whisper model"""
        logger.info(f"Loading Whisper model {self.model_size} on {self.device}")
        self.model = whisper.load_model(self.model_size, device=self.device)
        logger.info("Whisper model loaded successfully")
    
    async def transcribe(self, audio_data: bytes, language: str = "en") -> str:
        """Convert audio to text using Whisper"""
        loop = asyncio.get_event_loop()
        # Run transcription in thread pool since Whisper is synchronous
        result = await loop.run_in_executor(
            None, 
            lambda: self.model.transcribe(
                audio_data, 
                language=language if language != "auto" else None
            )
        )
        return result["text"].strip()
    
    def get_supported_languages(self) -> List[str]:
        """Get languages supported by Whisper"""
        return [
            "en", "es", "fr", "de", "zh", "ar", "hi", "ru", "pt", "it",
            "ja", "ko", "tur", "pl", "vi", "ta", "th", "la", "sw", "ha", "yo"
        ]


# Convenience function

def create_asr(model_size: str = "base", device: str = "cpu") -> WhisperASR:
    """Create a Whisper ASR instance"""
    return WhisperASR(model_size=model_size, device=device)