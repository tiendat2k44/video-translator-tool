"""
Module for extracting audio from video
"""
import subprocess
from pathlib import Path
from utils.logger import logger
import config


class AudioExtractor:
    def __init__(self):
        self.ffmpeg = config.FFMPEG_EXECUTABLE
        self.ffprobe = config.FFPROBE_EXECUTABLE

    def extract(self, video_path, output_audio_path=None, sample_rate=16000):
        """
        Extract audio from video using FFmpeg
        
        Args:
            video_path (str): Path to video file
            output_audio_path (str): Output audio file path (WAV format)
            sample_rate (int): Audio sample rate (default: 16000 Hz for Whisper)
        
        Returns:
            Path: Path to extracted audio file
        """
        try:
            video_path = Path(video_path)
            if not video_path.exists():
                raise FileNotFoundError(f"Video file not found: {video_path}")
            
            if output_audio_path is None:
                output_audio_path = video_path.parent / f"{video_path.stem}_audio.wav"
            
            output_audio_path = Path(output_audio_path)
            
            logger.info(f"🎵 Extracting audio from: {video_path.name}")
            
            cmd = [
                self.ffmpeg,
                "-i", str(video_path),
                "-q:a", "9",
                "-acodec", "libmp3lame",
                "-ar", str(sample_rate),
                "-ac", "1",  # Mono
                "-y",  # Overwrite
                str(output_audio_path)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=config.TRANSCRIPTION_TIMEOUT
            )
            
            if result.returncode != 0:
                logger.error(f"✗ FFmpeg error: {result.stderr}")
                raise Exception(f"FFmpeg error: {result.stderr}")
            
            if not output_audio_path.exists():
                raise Exception("Audio extraction failed: Output file not created")
            
            file_size = output_audio_path.stat().st_size / (1024 * 1024)
            logger.info(f"✓ Audio extracted: {output_audio_path.name} ({file_size:.2f} MB)")
            
            return output_audio_path
        
        except Exception as e:
            logger.error(f"✗ Error extracting audio: {e}")
            raise


__all__ = ["AudioExtractor"]
