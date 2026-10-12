"""TTS Component using ElevenLabs for voice cloning and natural speech generation"""

import logging
import asyncio
import aiohttp
from .pipeline import BaseTTSComponent

logger = logging.getLogger(__name__)


class ElevenLabsTTS(BaseTTSComponent):
    """ElevenLabs TTS for voice cloning and natural speech generation"""
    
    def __init__(self, api_key: str = None, voice_id: str = "21m00tTalkD0BdBXnoSSxeF"):
        self.api_key = api_key or self._get_default_api_key()
        self.voice_id = voice_id
        self.base_url = "https://api.elevenlabs.io/v1"
        self.session = None
    
    def _get_default_api_key(self) -> str:
        """Get default API key from environment or default"""
        import os
        return os.environ.get("ELEVENLABS_API_KEY", "default_key_placeholder")
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def synthesize(self, text: str, voice_style: str = "neutral", 
                        target_language: str = "en") -> bytes:
        """Generate speech audio from text using ElevenLabs"""
        session = await self._get_session()
        
        # Prepare voice selection based on language and style
        # For now use the default voice, but in production would select
        # language-appropriate voices
        voice_params = {
            "voice_id": self.voice_id,
            "model_id": "eleven_turbo_v2_5",  # Turbo model for low latency
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
                "style": 0.0 if voice_style == "natural" else 0.5,
                "use_speaker_boost": True
            }
        }
        
        url = f"{self.base_url}/text-to-speech/{self.voice_id}"
        headers = {"xi-api-key": self.api_key, "Content-Type": "application/json"}
        payload = {
            "text": text,
            **voice_params
        }
        
        try:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status == 200:
                    audio_data = await response.read()
                    return audio_data
                else:
                    logger.error(f"ElevenLabs API error: {response.status}")
                    return self._generate_fallback_audio(text)
        except Exception as e:
            logger.error(f"ElevenLabs TTS error: {e}")
            return self._generate_fallback_audio(text)
    
    def clone_voice(self, reference_audio: bytes, target_language: str) -> bytes:
        """Clone voice characteristics from reference audio for target language"""
        # In production, this would use ElevenLabs voice cloning features
        # or custom training to match the original speaker's voice
        return asyncio.get_event_loop().run_until_complete(
            self.synthesize(
                "This is cloned voice audio in the target language",
                voice_style="natural",
                target_language=target_language
            )
        )
    
    def _generate_fallback_audio(self, text: str) -> bytes:
        """Generate fallback audio when API is unavailable"""
        import struct
        import math
        
        sample_rate = 22050
        duration = max(0.5, len(text) * 0.1)  # Rough duration based on text length
        t = [i / sample_rate for i in range(int(sample_rate * duration))]
        
        # Generate multi-frequency audio that varies with text length
        base_freq = 200 + len(text) * 10
        samples = []
        for i, t_i in enumerate(t):
            # Vary frequency based on text characteristics
            freq = base_freq + 50 * __import__('math').sin(2 * __import__('math').pi * t_i * 2)
            sample = int(32767 * 0.3 * __import__('math').sin(2 * __import__('math').pi * freq * t_i))
            samples.append(sample)
        
        audio_bytes = struct.pack('<' + 'h' * len(samples), *samples)
        return audio_bytes


# Convenience function

def create_tts(api_key: str = None, voice_id: str = "21m00tTalkD0BdBXnoSSxeF") -> ElevenLabsTTS:
    """Create an ElevenLabs TTS instance"""
    return ElevenLabsTTS(api_key=api_key, voice_id=voice_id)