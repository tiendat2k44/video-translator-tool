"""
Module for creating subtitles in SRT and VTT formats
"""
from pathlib import Path
from utils.logger import logger
from utils.helpers import seconds_to_srt_time
import pysrt


class SubtitleMaker:
    def __init__(self):
        pass

    def create_srt(self, segments, output_path):
        """
        Create SRT subtitle file from segments
        
        Args:
            segments (list): List of segments with 'start', 'end', 'text'
            output_path (str): Output SRT file path
        
        Returns:
            Path: Path to created SRT file
        """
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"📝 Creating SRT subtitle: {output_path.name}")
            
            subs = pysrt.SubRipFile()
            
            for idx, seg in enumerate(segments, 1):
                sub = pysrt.SubRip()
                sub.index = idx
                sub.start = pysrt.SubRipTime(seconds=seg['start'])
                sub.end = pysrt.SubRipTime(seconds=seg['end'])
                sub.content = seg['text']
                
                subs.append(sub)
            
            subs.save(str(output_path), encoding='utf-8')
            
            logger.info(f"✓ SRT created: {len(subs)} subtitles")
            return output_path
        
        except Exception as e:
            logger.error(f"✗ Error creating SRT: {e}")
            raise

    def create_vtt(self, segments, output_path):
        """
        Create VTT subtitle file from segments
        
        Args:
            segments (list): List of segments
            output_path (str): Output VTT file path
        
        Returns:
            Path: Path to created VTT file
        """
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"📝 Creating VTT subtitle: {output_path.name}")
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("WEBVTT\n\n")
                
                for seg in segments:
                    start = seconds_to_srt_time(seg['start']).replace(',', '.')
                    end = seconds_to_srt_time(seg['end']).replace(',', '.')
                    f.write(f"{start} --> {end}\n")
                    f.write(f"{seg['text']}\n\n")
            
            logger.info(f"✓ VTT created: {len(segments)} subtitles")
            return output_path
        
        except Exception as e:
            logger.error(f"✗ Error creating VTT: {e}")
            raise

    def create_bilingual_srt(self, segments_original, segments_translated, output_path):
        """
        Create bilingual SRT with original and translated text
        
        Args:
            segments_original (list): Original segments
            segments_translated (list): Translated segments
            output_path (str): Output SRT file path
        
        Returns:
            Path: Path to created SRT file
        """
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"📝 Creating bilingual SRT: {output_path.name}")
            
            subs = pysrt.SubRipFile()
            
            for idx, (seg_orig, seg_trans) in enumerate(zip(segments_original, segments_translated), 1):
                sub = pysrt.SubRip()
                sub.index = idx
                sub.start = pysrt.SubRipTime(seconds=seg_orig['start'])
                sub.end = pysrt.SubRipTime(seconds=seg_orig['end'])
                # Format: Original text / Translated text
                sub.content = f"{seg_orig['text']}\n{seg_trans['text']}"
                
                subs.append(sub)
            
            subs.save(str(output_path), encoding='utf-8')
            
            logger.info(f"✓ Bilingual SRT created: {len(subs)} subtitles")
            return output_path
        
        except Exception as e:
            logger.error(f"✗ Error creating bilingual SRT: {e}")
            raise

    def parse_srt(self, srt_path):
        """
        Parse existing SRT file
        
        Args:
            srt_path (str): Path to SRT file
        
        Returns:
            list: List of segments
        """
        try:
            subs = pysrt.load(str(srt_path), encoding='utf-8')
            
            segments = []
            for sub in subs:
                segments.append({
                    'start': sub.start.total_seconds(),
                    'end': sub.end.total_seconds(),
                    'text': sub.content,
                })
            
            logger.info(f"✓ Parsed SRT: {len(segments)} subtitles")
            return segments
        
        except Exception as e:
            logger.error(f"✗ Error parsing SRT: {e}")
            raise


__all__ = ["SubtitleMaker"]
