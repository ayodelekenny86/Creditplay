"""FastAPI endpoint for AI Live Translation Broadcast Pipeline"""

import asyncio
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any

from src.pipeline import BroadcastPipeline, BroadcastInput, TranslationResult
from src.asr.rule_based_asr import create_asr as rule_asr
from src.translation.rule_based_nmt import create_nmt as rule_nmt
from src.tts.rule_based_tts import create_tts as rule_tts
from src.lip_sync.rule_based_lipsync import create_lip_sync as rule_lipsync

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Live Translation & Lip Sync Broadcast",
    version="1.0.0",
    description="Real-time AI translation with voice cloning and lip sync for broadcasts"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize pipeline components
asr_model = rule_asr()
nmt_model = rule_nmt()
tts_model = rule_tts()
lip_sync_model = rule_lipsync()

# Create the main pipeline
pipeline = BroadcastPipeline(
    asr=asr_model,
    nmt=nmt_model,
    tts=tts_model,
    lip_sync=lip_sync_model
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Live Translation & Lip Sync Broadcast API",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "components": {
            "asr": "ready",
            "nmt": "ready",
            "tts": "ready",
            "lip_sync": "ready"
        }
    }


@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...), language: str = "en"):
    """Transcribe audio using ASR"""
    try:
        audio_data = await file.read()
        text = await pipeline.asr.transcribe(audio_data, language)
        return {
            "success": True,
            "original_text": text,
            "language": language,
            "audio_size": len(audio_data)
        }
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/translate/")
async def translate_text(
    text: str,
    target_language: str,
    source_language: str = "en"
):
    """Translate text using NMT"""
    try:
        translated = await pipeline.nmt.translate(text, target_language, source_language)
        return {
            "success": True,
            "original_text": text,
            "translated_text": translated,
            "target_language": target_language,
            "source_language": source_language
        }
    except Exception as e:
        logger.error(f"Translation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tts/")
async def text_to_speech(
    text: str,
    voice_style: str = "natural",
    target_language: str = "en"
):
    """Generate speech using TTS"""
    try:
        audio_bytes = await pipeline.tts.synthesize(
            text, voice_style=voice_style, target_language=target_language
        )
        return {
            "success": True,
            "audio_size": len(audio_bytes),
            "target_language": target_language,
            "voice_cloned": True
        }
    except Exception as e:
        logger.error(f"TTS error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/lipsync/")
async def lip_sync_video(
    video: UploadFile = File(...),
    audio: UploadFile = File(...)
):
    """Apply lip sync to video"""
    try:
        video_data = await video.read()
        audio_data = await audio.read()
        synced_video = await pipeline.lip_sync.sync_lip_movements(video_data, audio_data)
        return {
            "success": True,
            "synced_video_size": len(synced_video),
            "lip_sync_applied": True
        }
    except Exception as e:
        logger.error(f"Lip sync error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/translate_broadcast/")
async def translate_broadcast(
    file: UploadFile = File(...),
    target_languages: str = "es,fr,de",
    include_lip_sync: bool = True
):
    """
    Full broadcast translation pipeline.
    Translates live broadcast audio/video into multiple languages
    with voice cloning and lip sync.
    """
    try:
        file_data = await file.read()
        lang_list = [lang.strip() for lang in target_languages.split(",")]
        
        broadcast_input = BroadcastInput(
            audio_data=file_data,
            video_data=file_data if file.content_type and 'video' in file.content_type else None,
            broadcast_id="temp_broadcast"
        )
        
        results = await pipeline.process_broadcast(broadcast_input, lang_list)
        
        response = {
            "success": True,
            "broadcast_id": broadcast_input.broadcast_id,
            "original_text": results[0].original_text if results else "",
            "target_languages": lang_list,
            "results": []
        }
        
        for result in results:
            result_summary = {
                "target_language": result.target_language,
                "original_text": result.original_text,
                "translated_text": result.translated_text,
                "confidence_score": result.confidence_score,
                "audio_cloned": result.audio_cloned,
                "lip_sync_ready": result.lip_sync_ready
            }
            response["results"].append(result_summary)
        
        return response
        
    except Exception as e:
        logger.error(f"Broadcast translation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/translate_clip/")
async def translate_clip(
    file: UploadFile = File(...),
    target_language: str = "es"
):
    """Translate a recorded clip"""
    try:
        file_data = await file.read()
        text = await pipeline.asr.transcribe(file_data, "en")
        translated = await pipeline.nmt.translate(text, target_language)
        audio = await pipeline.tts.synthesize(translated, target_language=target_language)
        
        return {
            "success": True,
            "original_text": text,
            "translated_text": translated,
            "target_language": target_language,
            "audio_generated": len(audio)
        }
    except Exception as e:
        logger.error(f"Clip translation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)