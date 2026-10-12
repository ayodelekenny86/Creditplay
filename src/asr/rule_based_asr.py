"""Rule-based ASR for demonstration purposes"""

import logging
from src.pipeline import BaseASRComponent

logger = logging.getLogger(__name__)


class RuleBasedASR(BaseASRComponent):
    """Rule-based ASR for demonstration purposes"""
    
    async def transcribe(self, audio_data: bytes, language: str = "en") -> str:
        """Convert audio to text (placeholder)"""
        return "Good evening viewers welcome to our broadcast"
    
    def get_supported_languages(self) -> list:
        return [
            "en", "es", "fr", "de", "zh", "ar", "hausa", "yoruba", "swahili"
        ]


# Convenience function

def create_asr() -> RuleBasedASR:
    """Create a rule-based ASR instance"""
    return RuleBasedASR()
