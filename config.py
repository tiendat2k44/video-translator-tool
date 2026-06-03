"""
Configuration file for Video Translator Tool
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Paths
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
TEMP_DIR = BASE_DIR / "temp"

# Create directories if not exists
OUTPUT_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

# Language mappings
LANGUAGE_MAP = {
    "zh": "Chinese (Simplified)",
    "zh-CN": "Chinese (Simplified)",
    "zh-TW": "Chinese (Traditional)",
    "ko": "Korean",
    "ja": "Japanese",
    "vi": "Vietnamese",
    "en": "English",
}

LANGUAGE_CODES = {
    "zh": "zh-CN",
    "ko": "ko",
    "ja": "ja",
    "vi": "vi",
    "en": "en",
}

# Video categories for translation style
CATEGORIES = {
    "movie": "Movie/Film",
    "drama": "Drama/TV Series",
    "comedy": "Comedy",
    "general": "General/Other",
    "anime": "Anime",
    "documentary": "Documentary",
    "music": "Music",
}

# Whisper model sizes
WHISPER_MODELS = {
    "tiny": "tiny",
    "base": "base",
    "small": "small",
    "medium": "medium",
    "large": "large",
}

# Default settings
DEFAULT_WHISPER_MODEL = "base"  # Balanced between speed and accuracy
DEFAULT_OUTPUT_FORMAT = "srt"  # srt or vtt
DEFAULT_AUDIO_QUALITY = "128"  # kbps
DEFAULT_VIDEO_QUALITY = "720"  # 720, 1080, 480, best

# API Configuration
GOOGLE_TRANSLATE_API_KEY = os.getenv("GOOGLE_TRANSLATE_API_KEY", "")
GOOGLE_TTS_API_KEY = os.getenv("GOOGLE_TTS_API_KEY", "")

# FFmpeg settings
FFMPEG_EXECUTABLE = os.getenv("FFMPEG_PATH", "ffmpeg")
FFPROBE_EXECUTABLE = os.getenv("FFPROBE_PATH", "ffprobe")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = BASE_DIR / "logs" / "app.log"
LOG_FILE.parent.mkdir(exist_ok=True)

# Bilibili specific
BILIBILI_REFERER = "https://www.bilibili.com/"
BILIBILI_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# Timeout settings (seconds)
DOWNLOAD_TIMEOUT = 300
TRANSCRIPTION_TIMEOUT = 3600
TRANSLATION_TIMEOUT = 600

# Audio extraction settings
AUDIO_SAMPLE_RATE = 16000  # Hz (required for Whisper)
AUDIO_CHANNELS = 1  # Mono

# Character encoding
DEFAULT_ENCODING = "utf-8"

print(f"✓ Configuration loaded from {BASE_DIR}")
