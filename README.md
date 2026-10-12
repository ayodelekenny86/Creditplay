"""
AI Live Translation & Lip Sync Broadcast - Setup and Installation

This project provides a complete AI-powered live translation and lip sync 
broadcast solution. It consists of multiple modules working together:

Core Components:
- ASR: Speech-to-text using OpenAI Whisper
- NMT: Neural machine translation using Hugging Face MarianMT
- TTS: Voice cloning and natural speech generation using ElevenLabs
- Lip Sync: Mouth movement synchronization using Wav2Lip
- Pipeline: Orchestrates all components for full broadcast translation

Installation:
-----------

1. Create a virtual environment (recommended):
   python3 -m venv venv
   source venv/bin/activate

2. Install dependencies:
   pip install -r requirements.txt

2. Set up API keys:
   - ElevenLabs API key for TTS voice cloning
   - Export as: export ELEVENLABS_API_KEY="your_key_here"

3. Run the API server:
   uvicorn src.api.main:app --host 0.0.0.0 --port 8000

4. Access the API at: http://localhost:8000

Available Endpoints:
-------------------
- GET  /          - Root endpoint
- GET  /health     - Health check
- POST /transcribe - Transcribe audio to text
- POST /translate  - Translate text to target language
- POST /tts        - Generate speech from text
- POST /lipsync    - Apply lip sync to video
- POST /translate_broadcast - Full broadcast translation pipeline
- POST /translate_clip - Translate recorded clip

Pipeline Workflow:
-----------------
1. Input Capture: Live broadcast audio/video fed into system
2. ASR: Speech recognition converts audio to text in real-time
3. NMT: Neural machine translation translates text to target language
4. TTS: Voice cloning generates natural speech in target language
5. Lip Sync: Mouth movements adjusted to match translated audio
6. Output Delivery: Translated, lip-synced video streamed back

Supported Features:
------------------
- Real-time AI translation into multiple languages simultaneously
- Voice cloning with natural tone and emotion matching
- Lip syncing to match mouth movements with translated speech
- Multi-dialect support (English, Hausa, Yoruba, Swahili, etc.)
- Offline/local deployment capability
- Multi-language feed outputs (e.g., English, Hausa, Yoruba, Swahili)
- Scalable integration with TV stations, streaming apps, and home videos

Deployment Options:
------------------
- TV Stations: Integrated directly into broadcast systems
- Streaming Platforms: Plugin for Netflix, YouTube, or local OTT apps
- Mobile/Radio Units: Lightweight version for rural areas
- Offline Mode: Pre-downloaded translation packs for poor connectivity

Performance Targets:
-------------------
- Latency: <2 seconds delay for real-time translation
- Supported Languages: 20+ languages including African dialects
- Audio Quality: Natural voice cloning with emotion preservation
- Lip Sync Quality: Realistic mouth movement synchronization

For more information, visit: https://github.com/ai-translation/broadcast-solution
"""

from . import __version__