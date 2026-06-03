# Installation Guide

## Prerequisites

- Python 3.8 or higher
- FFmpeg installed and in PATH
- Git (for cloning repository)

### Install FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from: https://ffmpeg.org/download.html

Or use Chocolatey:
```bash
choco install ffmpeg
```

Verify installation:
```bash
ffmpeg -version
```

## Setup

### 1. Clone Repository
```bash
git clone https://github.com/tiendat2k44/video-translator-tool.git
cd video-translator-tool
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys (Optional)

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys if you want to use Google Cloud services:
```
GOOGLE_TRANSLATE_API_KEY=your_key_here
GOOGLE_TTS_API_KEY=your_key_here
```

**Note:** The tool uses free alternatives by default:
- **Translation:** Google Translate (free)
- **Speech Recognition:** Whisper (free, offline)
- **Text-to-Speech:** gTTS (free)

## Quick Start

### Create Vietnamese Subtitles (Chinese Video)
```bash
python main.py translate \
  --url "https://www.bilibili.com/video/BV1xxx" \
  --source-lang zh \
  --subtitle-only
```

### Create Vietnamese Dubbed Video (Japanese Anime)
```bash
python main.py translate \
  --url "https://www.bilibili.com/video/BV1xxx" \
  --source-lang ja \
  --category anime \
  --with-dubbing
```

### Create Subtitles Only (Korean Video)
```bash
python main.py subtitle \
  --url "https://www.bilibili.com/video/BV1xxx" \
  --source-lang ko
```

### Create Dubbed Version (Movie)
```bash
python main.py dub \
  --url "https://www.bilibili.com/video/BV1xxx" \
  --source-lang zh \
  --category movie
```

## View Available Languages and Categories

```bash
python main.py info
```

## Output

Results are saved in `output/` directory:

```
output/
├── video.mp4                    # Original downloaded video
├── audio.wav                    # Extracted audio
├── transcription.json           # Speech recognition results
├── subtitle_vi.srt              # Vietnamese subtitles
├── video_with_subtitle.mp4      # Video with embedded subtitles
├── dubbed_audio.mp3             # Vietnamese dubbed audio
├── video_vi_dubbed_final.mp4    # Final dubbed video
└── results.json                 # Pipeline results summary
```

## Troubleshooting

### FFmpeg not found
- Make sure FFmpeg is installed and in PATH
- On Windows, restart terminal after installation

### Whisper model download fails
- Models are downloaded on first use
- Internet connection required
- Models stored in `~/.cache/whisper/`

### Translation API errors
- Check `.env` file configuration
- Verify API keys are valid
- Tool falls back to free alternatives

## Performance Tips

1. **Speed up processing:**
   - Use `--subtitle-only` flag if you don't need dubbing
   - Download high-quality videos (1080p) for better transcription

2. **Reduce file size:**
   - Reduce `--video-quality` to 480p for faster processing
   - Lower bitrate for audio files

3. **Better accuracy:**
   - Choose correct `--source-lang` for transcription
   - Use category flag to improve translation style

## License

MIT License - See LICENSE file
