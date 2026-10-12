"""Rule-based NMT for demonstration purposes"""

import asyncio
import logging
from src.pipeline import BaseNMTComponent

logger = logging.getLogger(__name__)


class RuleBasedNMT(BaseNMTComponent):
    """Rule-based NMT for demonstration purposes"""
    
    async def translate(self, text: str, target_language: str, 
                        source_language: str = "en") -> str:
        """Translate text to target language (placeholder)"""
        translations = {
            "es": "Buenas noches, televidentes. Bienvenidos a nuestro programa de transmisión.",
            "fr": "Bonsoir, téléspectateurs. Bienvenue dans notre émission de diffusion.",
            "de": "Guten Abend, Zuschauer. Willkommen bei unserer Sendung.",
            "zh": "晚上好，观众欢迎收看我们的广播节目。",
            "ar": "مساء الخير للمتابعين. أهلاً بكم في بثنا.",
            "hausa": "Nana liyanki, auduwar kan ya fascen samu ba.",
            "yoruba": "E ààyé, a kanmọ́. Ẹ ṣeẸ jẹ́ àgbáyé àlàyé.",
            "swahili": "Usiku mwema, wategemezi. Karibu katika eneo langu la msumari."
        }
        
        return translations.get(target_language, text)
    
    def get_supported_target_languages(self) -> list:
        return ["es", "fr", "de", "zh", "ar", "hausa", "yoruba", "swahili"]


# Convenience function

def create_nmt() -> RuleBasedNMT:
    """Create a rule-based NMT instance"""
    return RuleBasedNMT()
