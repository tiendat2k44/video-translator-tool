# Video Translator Tool 🎬🌍

Tool tải video từ Bilibili, nhận diện giọng nói, dịch và tạo phụ đề đa ngôn ngữ sang tiếng Việt.

## 🎯 Tính năng

- ✅ Tải video từ Bilibili (yt-dlp)
- ✅ Trích xuất âm thanh (FFmpeg)
- ✅ Nhận diện giọng nói (OpenAI Whisper)
- ✅ Dịch máy tự động (Google Translate)
- ✅ Tạo phụ đề (SRT/VTT)
- ✅ Lồng tiếng (TTS - Google Text-to-Speech)
- ✅ Hỗ trợ ngôn ngữ: Trung (中文), Hàn (한국어), Nhật (日本語) → Việt (Tiếng Việt)
- ✅ Phân loại dịch: Phim, Kịch, Hài, Tổng hợp, v.v.

## 📋 Yêu cầu hệ thống

- Python 3.8+
- FFmpeg
- Whisper (OpenAI)

## 🚀 Cài đặt

```bash
# Clone repository
git clone https://github.com/tiendat2k44/video-translator-tool.git
cd video-translator-tool

# Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Cài đặt dependencies
pip install -r requirements.txt

# Cài đặt FFmpeg
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows (hoặc download từ https://ffmpeg.org/download.html)
choco install ffmpeg
```

## 💻 Sử dụng

### CLI Command
```bash
python main.py --url "https://www.bilibili.com/video/BV..." \
               --source-lang "zh" \
               --output-lang "vi" \
               --category "movie" \
               --output-dir "./output"
```

### Tham số
- `--url`: Link video Bilibili
- `--source-lang`: Ngôn ngữ gốc (zh, ko, ja)
- `--output-lang`: Ngôn ngữ đích (vi)
- `--category`: Phân loại (movie, drama, comedy, general)
- `--output-dir`: Thư mục output
- `--subtitle-only`: Chỉ tạo phụ đề (không lồng tiếng)
- `--with-dubbing`: Tạo video lồng tiếng

### Ví dụ

```bash
# Tạo phụ đề tiếng Việt từ video tiếng Trung
python main.py translate --url "https://www.bilibili.com/video/BV1xxx" \
               --source-lang "zh" \
               --subtitle-only

# Tạo phụ đề + video lồng tiếng
python main.py translate --url "https://www.bilibili.com/video/BV1xxx" \
               --source-lang "ja" \
               --with-dubbing
```

## 📁 Cấu trúc thư mục

```
video-translator-tool/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── config.py              # Configuration
├── modules/
│   ├── downloader.py      # Tải video Bilibili
│   ├── audio_extractor.py # Trích xuất âm thanh
│   ├── transcriber.py     # Nhận diện giọng nói (Whisper)
│   ├── translator.py      # Dịch máy (Google Translate)
│   ├── subtitle_maker.py  # Tạo phụ đề (SRT/VTT)
│   ├── tts_engine.py      # Lồng tiếng (TTS)
│   ├── merger.py          # Ghép video + audio
│   ├── video_translator.py # Mix audio
│   └── pipeline.py        # Orchestrator
├── utils/
│   ├── logger.py          # Logging
│   └── helpers.py         # Hàm hỗ trợ
└── output/                # Thư mục output
```

## 🛠️ API sử dụng

| Công cụ | Miễn phí | Tốc độ | Ghi chú |
|---------|---------|-------|----------|
| yt-dlp | ✅ | ⚡⚡ | Tải video Bilibili |
| FFmpeg | ✅ | ⚡⚡⚡ | Xử lý âm thanh/video |
| Whisper | ✅ | ⚡ | Nhận diện giọng nói |
| Google Translate | ✅ | ⚡⚡ | Dịch máy |
| Google TTS | ✅ | ⚡⚡ | Lồng tiếng |

## 📝 Ví dụ Output

```
output/
├── video.mp4              # Video gốc
├── audio.wav              # Âm thanh trích xuất
├── transcription.json     # Kịch bản nhận diện
├── subtitle_vi.srt        # Phụ đề tiếng Việt
├── audio_vi.mp3           # Âm thanh lồng tiếng Việt
└── video_vi_dubbed.mp4    # Video lồng tiếng hoàn chỉnh
```

## ⚠️ Lưu ý

- Chỉ hỗ trợ video công khai trên Bilibili
- Không hỗ trợ nội dung có DRM/bản quyền
- Tôn trọng bản quyền của tác giả gốc
- Tải về để học tập và mục đích cá nhân

## 📧 Liên hệ

- GitHub: [@tiendat2k44](https://github.com/tiendat2k44)

## 📄 License

MIT License - Xem file LICENSE để biết chi tiết
