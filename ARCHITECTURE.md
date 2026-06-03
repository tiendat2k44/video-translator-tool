# Architecture Documentation

## System Overview

```
Bilibili Video → Download → Audio Extract → Transcribe → Translate → TTS → Merge → Output
```

## Module Structure

### 1. **Downloader Module** (`modules/downloader.py`)
- **Purpose:** Download videos from Bilibili
- **Tool:** yt-dlp
- **Features:**
  - Support for various video qualities
  - Optional subtitle download
  - Automatic error handling
- **Output:** MP4 video file

### 2. **Audio Extractor** (`modules/audio_extractor.py`)
- **Purpose:** Extract audio from video
- **Tool:** FFmpeg
- **Features:**
  - Mono conversion (required for Whisper)
  - 16kHz sample rate (Whisper standard)
  - Multiple format support
- **Output:** WAV audio file

### 3. **Transcriber** (`modules/transcriber.py`)
- **Purpose:** Speech-to-text conversion
- **Tool:** OpenAI Whisper
- **Features:**
  - Multiple model sizes (tiny → large)
  - Language detection
  - Timestamp generation
  - Supports Chinese, Japanese, Korean
- **Output:** Segments with text and timestamps

### 4. **Translator** (`modules/translator.py`)
- **Purpose:** Translate text to Vietnamese
- **Tool:** Google Translate (with fallback)
- **Features:**
  - Batch translation support
  - Language detection
  - Free API access
  - Fallback to googletrans library
- **Output:** Translated text segments

### 5. **Subtitle Maker** (`modules/subtitle_maker.py`)
- **Purpose:** Create subtitle files
- **Formats:** SRT, VTT
- **Features:**
  - Bilingual subtitle support
  - Automatic timing calculation
  - UTF-8 encoding
- **Output:** SRT/VTT files

### 6. **TTS Engine** (`modules/tts_engine.py`)
- **Purpose:** Generate dubbed audio
- **Tools:** Google Cloud TTS, gTTS (fallback)
- **Features:**
  - Multiple voice options
  - Batch processing
  - MP3 output
  - Natural pronunciation
- **Output:** MP3 audio files

### 7. **Video Merger** (`modules/merger.py`)
- **Purpose:** Combine video, audio, and subtitles
- **Tool:** FFmpeg
- **Features:**
  - Audio replacement
  - Subtitle embedding
  - Multiple audio tracks
- **Output:** Final MP4 video

### 8. **Audio Mixer** (`modules/video_translator.py`)
- **Purpose:** Mix multiple audio segments
- **Tool:** pydub
- **Features:**
  - Precise timing
  - Audio synchronization
  - Format conversion
- **Output:** Mixed audio file

### 9. **Translation Pipeline** (`modules/pipeline.py`)
- **Purpose:** Orchestrate entire workflow
- **Features:**
  - Full pipeline execution
  - Subtitle-only mode
  - Dubbing mode
  - Error recovery
- **Output:** Complete results dictionary

## Data Flow

```
INPUT: Bilibili URL
  ↓
[BilibiliDownloader]
  ↓
Video File
  ↓
[AudioExtractor]
  ↓
Audio File
  ↓
[Transcriber]
  ↓
Segments (text + timestamps)
  ↓
[Translator]
  ↓
Translated Segments
  ↓
[SubtitleMaker] ←→ [TTSEngine]
  ↓              ↓
Subtitle File   Audio Files
  ↓              ↓
[VideoMerger] ←→ [AudioMixer]
  ↓
Final Output (Video + Subtitle + Dubbed Audio)
```

## Configuration System

- **config.py**: Central configuration
- **.env.example**: Environment variables template
- **Language mappings**: Bilibili language codes
- **Category definitions**: Video type classification
- **Model settings**: Whisper, FFmpeg parameters

## Utility Modules

### Logger (`utils/logger.py`)
- Loguru-based logging system
- Console and file output
- Automatic rotation

### Helpers (`utils/helpers.py`)
- Time conversion (SRT format)
- URL parsing
- File validation
- JSON handling

## Error Handling

- Try-catch blocks in each module
- Logging at error/warning/info levels
- Graceful fallbacks (e.g., gTTS if Google Cloud fails)
- File existence verification

## Performance Considerations

1. **Memory Usage:**
   - Large video files buffered by FFmpeg
   - Whisper model cached after first load
   - Audio segments processed sequentially

2. **Processing Time:**
   - Download: 1-5 minutes (depends on video length)
   - Audio extraction: 10-30 seconds
   - Transcription: 1-10 minutes (depends on audio length)
   - Translation: 1-5 minutes
   - TTS: 2-10 minutes
   - Merging: 5-15 minutes

3. **Optimization Tips:**
   - Use smaller Whisper models for speed
   - Process only subtitles (skip TTS)
   - Lower video quality for faster processing

## Language Support

| Language | Code | Module | Notes |
|----------|------|--------|-------|
| Chinese | zh | Transcriber, Translator | Simplified Chinese |
| Japanese | ja | Transcriber, Translator | Standard Japanese |
| Korean | ko | Transcriber, Translator | Standard Korean |
| Vietnamese | vi | Translator, TTS | Output language |

## Extensibility

The modular design allows for easy extensions:

1. **Add new transcriber:**
   - Implement `transcribe()` method
   - Add to pipeline

2. **Add new translator:**
   - Implement `translate()` method
   - Update translator.py

3. **Add new TTS engine:**
   - Implement `synthesize()` method
   - Add language mapping

4. **Support new languages:**
   - Add to LANGUAGE_MAP in config.py
   - Add TTS voice mapping
   - Test with Whisper and Translator

## Testing

Recommended test cases:
- Short video (< 1 min)
- Different languages (zh, ja, ko)
- Different categories (movie, drama, comedy)
- Subtitle-only mode
- Full dubbing mode
- Error scenarios (invalid URL, network issues)

## Security Considerations

- No credentials stored in code
- API keys in .env file (not committed)
- Input validation for URLs
- Output file validation
- Logging sanitization (no sensitive data)

## Future Improvements

1. Parallel processing for batch operations
2. GPU acceleration for Whisper
3. Custom voice synthesis
4. Web UI interface
5. API server mode
6. Docker containerization
7. Support for more platforms (YouTube, etc.)
8. Advanced subtitle editing
9. Quality metrics and validation
10. Streaming processing for large files
