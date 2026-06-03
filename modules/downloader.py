"""
Module for downloading videos from Bilibili
"""
import subprocess
from pathlib import Path
from utils.logger import logger
import config


class BilibiliDownloader:
    def __init__(self, output_dir=None):
        self.output_dir = Path(output_dir) or config.OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def download(self, video_url, quality="720"):
        """
        Download video from Bilibili using yt-dlp
        
        Args:
            video_url (str): Bilibili video URL
            quality (str): Video quality (best, 1080, 720, 480, worst)
        
        Returns:
            Path: Path to downloaded video
        """
        try:
            logger.info(f"🔽 Downloading video from: {video_url}")
            
            output_template = str(self.output_dir / "%(title)s.%(ext)s")
            
            # Build yt-dlp command
            cmd = [
                "yt-dlp",
                "-f", f"bestvideo[height<={quality}]+bestaudio/best",
                "-o", output_template,
                "--merge-output-format", "mp4",
                "-q",
                video_url
            ]
            
            logger.debug(f"Command: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=config.DOWNLOAD_TIMEOUT
            )
            
            if result.returncode != 0:
                logger.error(f"✗ Download failed: {result.stderr}")
                raise Exception(f"yt-dlp error: {result.stderr}")
            
            # Find downloaded file
            video_files = list(self.output_dir.glob("*.mp4"))
            if not video_files:
                raise Exception("No video file found after download")
            
            video_path = video_files[-1]  # Get latest file
            file_size = video_path.stat().st_size / (1024 * 1024)
            logger.info(f"✓ Downloaded: {video_path.name} ({file_size:.2f} MB)")
            
            return video_path
        
        except subprocess.TimeoutExpired:
            logger.error(f"✗ Download timeout after {config.DOWNLOAD_TIMEOUT}s")
            raise
        except Exception as e:
            logger.error(f"✗ Error downloading video: {e}")
            raise

    def download_with_subtitle(self, video_url, quality="720"):
        """
        Download video with original subtitles if available
        
        Args:
            video_url (str): Bilibili video URL
            quality (str): Video quality
        
        Returns:
            tuple: (video_path, subtitle_path or None)
        """
        try:
            logger.info(f"🔽 Downloading video with subtitles...")
            
            output_template = str(self.output_dir / "%(title)s.%(ext)s")
            
            cmd = [
                "yt-dlp",
                "-f", f"bestvideo[height<={quality}]+bestaudio/best",
                "-o", output_template,
                "--merge-output-format", "mp4",
                "--write-subs",
                "--skip-unavailable-fragments",
                "-q",
                video_url
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=config.DOWNLOAD_TIMEOUT
            )
            
            if result.returncode != 0:
                logger.error(f"✗ Download failed: {result.stderr}")
                raise Exception(f"yt-dlp error: {result.stderr}")
            
            video_files = list(self.output_dir.glob("*.mp4"))
            subtitle_files = list(self.output_dir.glob("*.vtt")) + list(self.output_dir.glob("*.srt"))
            
            video_path = video_files[-1] if video_files else None
            subtitle_path = subtitle_files[-1] if subtitle_files else None
            
            if video_path:
                logger.info(f"✓ Downloaded: {video_path.name}")
            if subtitle_path:
                logger.info(f"✓ Found subtitle: {subtitle_path.name}")
            
            return video_path, subtitle_path
        
        except Exception as e:
            logger.error(f"✗ Error downloading video with subtitles: {e}")
            raise


__all__ = ["BilibiliDownloader"]
