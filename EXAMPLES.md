"""
Advanced usage examples for Video Translator Tool
"""

# Example 1: Create Vietnamese subtitles from Chinese video
# =========================================================
# Command:
# python main.py translate \
#   --url "https://www.bilibili.com/video/BV1Ab4y197mw" \
#   --source-lang zh \
#   --subtitle-only \
#   --output-dir ./my_output

# This will:
# 1. Download the Bilibili video
# 2. Extract audio
# 3. Recognize Chinese speech using Whisper
# 4. Translate to Vietnamese using Google Translate
# 5. Create SRT subtitles
# Result: Vietnamese subtitles in ./my_output/subtitle_vi.srt


# Example 2: Create fully dubbed Japanese anime to Vietnamese
# ===========================================================
# Command:
# python main.py dub \
#   --url "https://www.bilibili.com/video/BV1xxx" \
#   --source-lang ja \
#   --category anime

# This will:
# 1. Download video
# 2. Extract audio
# 3. Recognize Japanese speech
# 4. Translate to Vietnamese
# 5. Generate Vietnamese TTS audio
# 6. Replace original audio with dubbed version
# 7. Add Vietnamese subtitles
# Result: Fully dubbed Vietnamese video


# Example 3: Create subtitles only (fast mode)
# =============================================
# Command:
# python main.py subtitle \
#   --url "https://www.bilibili.com/video/BV1xxx" \
#   --source-lang ko

# Fastest option - only creates subtitles without dubbing


# Example 4: Using Python API directly
# ====================================
if __name__ == "__main__":
    from modules import TranslationPipeline
    from pathlib import Path
    
    # Initialize pipeline
    output_dir = Path("./my_output")
    pipeline = TranslationPipeline(output_dir)
    
    # Run subtitle-only mode
    results = pipeline.run_subtitle_only(
        video_url="https://www.bilibili.com/video/BV1xxx",
        source_lang="zh",
        target_lang="vi"
    )
    
    print(f"Subtitle saved to: {results['outputs']['subtitle']}")
    
    
    # Or run full dubbing pipeline
    results = pipeline.run_with_dubbing(
        video_url="https://www.bilibili.com/video/BV1xxx",
        source_lang="ja",
        target_lang="vi",
        category="anime"
    )
    
    print(f"Dubbed video: {results['outputs'].get('final_video')}")


# Example 5: Batch process multiple videos
# =========================================
if __name__ == "__main__":
    from modules import TranslationPipeline
    from pathlib import Path
    
    videos = [
        ("https://www.bilibili.com/video/BV1xxx", "zh"),
        ("https://www.bilibili.com/video/BV2xxx", "ja"),
        ("https://www.bilibili.com/video/BV3xxx", "ko"),
    ]
    
    output_base = Path("./batch_output")
    
    for video_url, source_lang in videos:
        print(f"\n Processing: {video_url}")
        output_dir = output_base / f"video_{len(output_base.glob('*'))}"
        
        pipeline = TranslationPipeline(output_dir)
        results = pipeline.run_subtitle_only(video_url, source_lang)
        
        print(f"✓ Completed: {results['outputs']['subtitle']}")


# Example 6: Custom translation with error handling
# =================================================
if __name__ == "__main__":
    from modules import TranslationPipeline
    from utils.logger import logger
    
    try:
        pipeline = TranslationPipeline()
        results = pipeline.run_full_pipeline(
            video_url="https://www.bilibili.com/video/BV1xxx",
            source_lang="zh",
            target_lang="vi",
            category="movie",
            with_dubbing=True,
            subtitle_only=False
        )
        
        logger.info(f"Success! Output: {results['outputs']}")
        
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        # Handle error appropriately
        pass


# Example 7: Using individual modules
# ====================================
if __name__ == "__main__":
    from modules import (
        BilibiliDownloader,
        AudioExtractor,
        Transcriber,
        Translator,
        SubtitleMaker
    )
    from pathlib import Path
    
    output_dir = Path("./custom_output")
    
    # Step 1: Download
    downloader = BilibiliDownloader(output_dir)
    video = downloader.download("https://www.bilibili.com/video/BV1xxx")
    
    # Step 2: Extract audio
    extractor = AudioExtractor()
    audio = extractor.extract(video)
    
    # Step 3: Transcribe
    transcriber = Transcriber(model_size="base")
    segments = transcriber.get_segments(audio, language="zh")
    
    # Step 4: Translate
    translator = Translator()
    translated = []
    for seg in segments:
        trans_text = translator.translate(seg['text'], "zh", "vi")
        translated.append({
            'start': seg['start'],
            'end': seg['end'],
            'text': trans_text
        })
    
    # Step 5: Create subtitles
    subtitle_maker = SubtitleMaker()
    srt_file = subtitle_maker.create_srt(translated, output_dir / "output.srt")
    
    print(f"Subtitle: {srt_file}")


# Example 8: Get video information before processing
# =================================================
if __name__ == "__main__":
    from modules import BilibiliDownloader
    
    # Check available:
    print("Supported languages:")
    from config import LANGUAGE_MAP, CATEGORIES
    
    for code, name in LANGUAGE_MAP.items():
        print(f"  {code}: {name}")
    
    print("\nSupported categories:")
    for code, name in CATEGORIES.items():
        print(f"  {code}: {name}")


# Example 9: Monitor progress with logging
# ========================================
if __name__ == "__main__":
    import logging
    from utils.logger import logger
    
    # Logging is automatically configured
    # Check logs in: logs/app.log
    
    # Different log levels:
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")


# Example 10: Performance optimization
# ===================================
# For faster processing:
# - Use --subtitle-only flag (skip TTS)
# - Lower video quality (480p instead of 1080p)
# - Use smaller Whisper model (tiny/base instead of large)
# - Increase system resources (RAM, CPU)

# For better quality:
# - Use larger Whisper model (medium/large)
# - Higher video quality (1080p)
# - Wait for full processing to complete
