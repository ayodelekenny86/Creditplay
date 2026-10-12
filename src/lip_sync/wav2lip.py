"""Lip Sync Component using Wav2Lip for mouth movement synchronization"""

import logging
import asyncio
import numpy as np
from .pipeline import BaseLipSyncComponent

logger = logging.getLogger(__name__)


class Wav2LipLipSync(BaseLipSyncComponent):
    """Wav2Lip for lip synchronization of video frames"""
    
    def __init__(self, fps: int = 30, face_detector_size: int = 96):
        self.fps = fps
        self.face_detector_size = face_detector_size
        self.model_loaded = False
        self._model_initialized = False
    
    def _initialize_model(self):
        """Initialize Wav2Lip model"""
        if self._model_initialized:
            return
        
        try:
            # Try to import wav2lip
            import sys
            sys.path.insert(0, '/workspace/app/src/lip_sync')
            
            # Check if wav2lip is available
            try:
                from wav2lip import load_wav2lip_model, lip_sync
                self.lip_sync_func = lip_sync
                self.load_model = load_wav2lip_model
                self.model_loaded = True
                logger.info("Wav2Lip model functions loaded successfully")
            except ImportError:
                logger.warning("Wav2Lip not available, using fallback")
                self.model_loaded = False
            
            self._model_initialized = True
        except Exception as e:
            logger.error(f"Wav2Lip initialization error: {e}")
            self.model_loaded = False
    
    async def sync_lip_movements(self, video_data: bytes, audio_data: bytes) -> bytes:
        """Adjust video mouth movements to match translated audio"""
        self._initialize_model()
        
        loop = asyncio.get_event_loop()
        
        try:
            # Run lip sync in thread pool
            result = await loop.run_in_executor(
                None,
                self._sync_lip_sync_sync,
                video_data,
                audio_data
            )
            return result
        except Exception as e:
            logger.error(f"Lip sync error: {e}")
            # Return original video as fallback
            return video_data
    
    def _sync_lip_sync_sync(self, video_data: bytes, audio_data: bytes) -> bytes:
        """Synchronous lip sync implementation"""
        self._initialize_model()
        
        if not self.model_loaded:
            return video_data
        
        try:
            # Save audio to temporary file
            import tempfile
            import os
            
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_audio:
                tmp_audio.write(audio_data)
                audio_path = tmp_audio.name
            
            with tempfile.NamedTemporaryFile(suffix='.avi', delete=False) as tmp_video:
                tmp_video.write(video_data)
                video_path = tmp_video.name
            
            try:
                # Run wav2lip lip sync
                output_path = audio_path.replace('.wav', '_synced.avi')
                self.lip_sync_func(video_path, audio_path, output_path)
                
                # Read synced video
                with open(output_path, 'rb') as f:
                    synced_video = f.read()
                
                return synced_video
            finally:
                # Cleanup temp files
                for path in [audio_path, video_path, output_path]:
                    if os.path.exists(path):
                        os.unlink(path)
                        
        except Exception as e:
            logger.error(f"Sync lip sync failed: {e}")
            return video_data
    
    def get_supported_languages(self) -> List[str]:
        """Get languages supported for lip sync"""
        return [
            "en", "es", "fr", "de", "zh", "ar", "hausa", "yoruba", "swahili",
            "ja", "ko", "pt", "ru", "it", "pl", "vi", "ta", "th"
        ]


# Convenience function

def create_lip_sync() -> Wav2LipLipSync:
    """Create a Wav2Lip lip sync instance"""
    return Wav2LipLipSync()