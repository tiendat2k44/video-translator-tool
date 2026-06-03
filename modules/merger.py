"""
Module for merging video and audio with FFmpeg
"""
import subprocess
from pathlib import Path
from utils.logger import logger
import config


class VideoMerger:
    def __init__(self):
        self.ffmpeg = config.FFMPEG_EXECUTABLE

    def merge_audio_to_video(self, video_path, audio_path, output_path=None, replace_audio=False):
        """
        Merge audio with video
        
        Args:
            video_path (str): Path to video file
            audio_path (str): Path to audio file
            output_path (str): Output video path
            replace_audio (bool): Replace original audio or add new track
        
        Returns:
            Path: Path to merged video
        """
        try:
            video_path = Path(video_path)
            audio_path = Path(audio_path)
            
            if not video_path.exists():
                raise FileNotFoundError(f"Video file not found: {video_path}")
            if not audio_path.exists():
                raise FileNotFoundError(f"Audio file not found: {audio_path}")
            
            if output_path is None:
                output_path = video_path.parent / f"{video_path.stem}_merged.mp4"
            
            output_path = Path(output_path)
            
            logger.info(f"🎬 Merging audio to video...")
            logger.debug(f"   Video: {video_path.name}")
            logger.debug(f"   Audio: {audio_path.name}")
            
            if replace_audio:
                # Replace original audio
                cmd = [
                    self.ffmpeg,
                    "-i", str(video_path),
                    "-i", str(audio_path),
                    "-c:v", "copy",
                    "-c:a", "aac",
                    "-map", "0:v:0",
                    "-map", "1:a:0",
                    "-shortest",
                    "-y",
                    str(output_path)
                ]
            else:
                # Add as secondary audio track
                cmd = [
                    self.ffmpeg,
                    "-i", str(video_path),
                    "-i", str(audio_path),
                    "-c:v", "copy",
                    "-c:a", "aac",
                    "-map", "0",
                    "-map", "1:a",
                    "-y",
                    str(output_path)
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
            
            if not output_path.exists():
                raise Exception("Merge failed: Output file not created")
            
            file_size = output_path.stat().st_size / (1024 * 1024)
            logger.info(f"✓ Video merged: {output_path.name} ({file_size:.2f} MB)")
            
            return output_path
        
        except Exception as e:
            logger.error(f"✗ Error merging audio to video: {e}")
            raise

    def add_subtitle_to_video(self, video_path, subtitle_path, output_path=None):
        """
        Embed subtitle into video
        
        Args:
            video_path (str): Path to video file
            subtitle_path (str): Path to subtitle file (SRT)
            output_path (str): Output video path
        
        Returns:
            Path: Path to video with embedded subtitle
        """
        try:
            video_path = Path(video_path)
            subtitle_path = Path(subtitle_path)
            
            if not video_path.exists():
                raise FileNotFoundError(f"Video file not found: {video_path}")
            if not subtitle_path.exists():
                raise FileNotFoundError(f"Subtitle file not found: {subtitle_path}")
            
            if output_path is None:
                output_path = video_path.parent / f"{video_path.stem}_subtitled.mp4"
            
            output_path = Path(output_path)
            
            logger.info(f"📝 Adding subtitle to video...")
            
            # FFmpeg filter for burning subtitle
            filter_complex = f"subtitles={subtitle_path.as_posix()}"
            
            cmd = [
                self.ffmpeg,
                "-i", str(video_path),
                "-vf", filter_complex,
                "-c:a", "copy",
                "-y",
                str(output_path)
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
            
            file_size = output_path.stat().st_size / (1024 * 1024)
            logger.info(f"✓ Subtitle added: {output_path.name} ({file_size:.2f} MB)")
            
            return output_path
        
        except Exception as e:
            logger.error(f"✗ Error adding subtitle: {e}")
            raise

    def create_dubbed_video(self, video_path, dubbed_audio_path, subtitle_path=None, output_path=None):
        """
        Create complete dubbed video with subtitle
        
        Args:
            video_path (str): Original video path
            dubbed_audio_path (str): Dubbed audio path
            subtitle_path (str): Subtitle path (optional)
            output_path (str): Output video path
        
        Returns:
            Path: Path to final dubbed video
        """
        try:
            logger.info(f"🎬 Creating dubbed video with subtitle...")
            
            # Step 1: Merge dubbed audio with video
            video_with_audio = self.merge_audio_to_video(
                video_path,
                dubbed_audio_path,
                replace_audio=True
            )
            
            # Step 2: Add subtitle if provided
            if subtitle_path:
                if output_path is None:
                    output_path = Path(video_path).parent / f"{Path(video_path).stem}_dubbed_final.mp4"
                
                final_video = self.add_subtitle_to_video(
                    video_with_audio,
                    subtitle_path,
                    output_path
                )
            else:
                final_video = video_with_audio
            
            logger.info(f"✓ Dubbed video completed: {final_video.name}")
            return final_video
        
        except Exception as e:
            logger.error(f"✗ Error creating dubbed video: {e}")
            raise


__all__ = ["VideoMerger"]
