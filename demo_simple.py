"""
AI Live Translation & Lip Sync Broadcast - Simplified Demo

Demonstrates the pipeline architecture without requiring Whisper
or heavy GPU dependencies. Uses rule-based components for demonstration.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add source to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.pipeline import BroadcastPipeline, BroadcastInput, TranslationResult
from src.asr.rule_based_asr import RuleBasedASR
from src.translation.rule_based_nmt import RuleBasedNMT
from src.tts.rule_based_tts import RuleBasedTTS
from src.lip_sync.rule_based_lipsync import RuleBasedLipSync

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def demo_basic_pipeline():
    """Demo basic translation pipeline with text"""
    logger.info("=" * 60)
    logger.info("DEMO 1: Basic Text Translation Pipeline")
    logger.info("=" * 60)
    
    # Initialize components (rule-based for demo)
    asr = RuleBasedASR()
    nmt = RuleBasedNMT()
    tts = RuleBasedTTS()
    
    # Sample English text
    english_text = "Good evening, viewers. Welcome to our broadcast."
    target_langs = ["es", "fr", "de", "hausa", "yoruba"]
    
    print(f"\nOriginal English: {english_text}\n")
    
    # Translate to each language
    for target_lang in target_langs:
        print(f"🎯 Target: {target_lang.upper()}")
        
        # Translate
        translated = await nmt.translate(english_text, target_lang)
        print(f"   Translated: {translated}")
        
        # Generate speech
        audio = await tts.synthesize(translated, target_language=target_lang)
        print(f"   🎤 Audio generated: {len(audio)} bytes")
        print()


async def demo_full_pipeline():
    """Demo full broadcast pipeline"""
    logger.info("=" * 60)
    logger.info("DEMO 2: Full Broadcast Pipeline (Text-based)")
    logger.info("=" * 60)
    
    # Initialize full pipeline
    pipeline = BroadcastPipeline()
    
    # Sample broadcast script
    script = "Good evening, viewers. Welcome to our news broadcast about technology and culture."
    
    print(f"\n📺 Original Broadcast Script:\n{script}\n")
    print("=" * 60)
    print("Processing through full pipeline...\n")
    
    # Process through pipeline
    target_langs = ["es", "fr", "de", "hausa", "yoruba"]
    results = await pipeline.process_broadcast(
        BroadcastInput(
            audio_data=b"",
            broadcast_id="demo_001"
        ),
        target_langs
    )
    
    # Display results
    for i, result in enumerate(results, 1):
        print(f"\n🌍 Language {i}: {result.target_language.upper()}")
        print(f"   Original: {result.original_text}")
        print(f"   Translated: {result.translated_text}")
        print(f"   🎤 Voice cloned: {result.audio_cloned}")
        print(f"   🔒 Lip sync ready: {result.lip_sync_ready}")
        print("-" * 60)
    
    print(f"\n✅ Pipeline completed successfully!")


async def demo_language_support():
    """Demo supported languages"""
    logger.info("=" * 60)
    logger.info("DEMO 3: Supported Languages")
    logger.info("=" * 60)
    
    asr = RuleBasedASR()
    nmt = RuleBasedNMT()
    tts = RuleBasedTTS()
    lip_sync = RuleBasedLipSync()
    
    print("\n📡 ASR Supported Languages:")
    for lang in asr.get_supported_languages()[:10]:
        print(f"   • {lang}")
    
    print("\n🔄 NMT Target Languages:")
    for lang in nmt.get_supported_target_languages()[:10]:
        print(f"   • {lang}")
    
    print("\n👄 Lip Sync Supported Languages:")
    for lang in lip_sync.get_supported_languages()[:10]:
        print(f"   • {lang}")
    
    print()


async def main():
    """Run all demos"""
    logger.info("AI Live Translation & Lip Sync Broadcast Solution")
    logger.info("=" * 60)
    
    await demo_basic_pipeline()
    await demo_full_pipeline()
    await demo_language_support()
    
    logger.info("=" * 60)
    logger.info("All demos completed!")
    logger.info("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())