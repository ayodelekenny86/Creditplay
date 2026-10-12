"""NMT Component using Hugging Face MarianMT for neural machine translation"""

import logging
from transformers import MarianMTModel, MarianTokenizer
from .pipeline import BaseNMTComponent

logger = logging.getLogger(__name__)


class HFMarianMT(BaseNMTComponent):
    """Hugging Face MarianMT for neural machine translation"""
    
    def __init__(self, model_name: str = "Helsinki-NLP/opus-mt-en"):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self._load_model()
    
    def _load_model(self):
        """Load MarianMT model and tokenizer"""
        logger.info(f"Loading MarianMT model: {self.model_name}")
        self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)
        self.model = MarianMTModel.from_pretrained(self.model_name)
        logger.info("MarianMT model loaded successfully")
    
    async def translate(self, text: str, target_language: str, 
                        source_language: str = "en") -> str:
        """Translate text to target language"""
        loop = asyncio.get_event_loop()
        
        # For MarianMT, we need to handle language codes
        # Model is English-centric, so source is always English
        if source_language != "en":
            # Simple approach: translate from English first, then could add reverse
            pass
        
        # Run translation in thread pool
        result = await loop.run_in_executor(
            None,
            lambda: self.model.generate(
                **self.tokenizer([text], return_tensors="pt", padding=True, truncation=True)
            )
        )
        
        # Decode result
        translated = self.tokenizer.decode(result[0], skip_special_tokens=True)
        return translated
    
    def get_supported_target_languages(self) -> List[str]:
        """Get target languages supported by this model"""
        # Common language codes for Opus-MT models
        return [
            "es", "fr", "de", "pt", "it", "pl", "ru", "ar", "zh", "ja",
            "ko", "tr", "vi", "ta", "th", "sw", "ha", "yo", "zu", "xh"
        ]


# Convenience function

def create_nmt(model_name: str = "Helsinki-NLP/opus-mt-en") -> HFMarianMT:
    """Create a MarianMT NMT instance"""
    return HFMarianMT(model_name=model_name)