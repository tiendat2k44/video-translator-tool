"""
Module for orchestrating the entire translation pipeline
"""
from pathlib import Path
from utils.logger import logger
from utils.helpers import create_output_structure, save_json, load_json
from modules.downloader import BilibiliDownloader
from modules.audio_extractor import AudioExtractor
from modules.transcriber import Transcriber
from modules.translator import Translator
from modules.subtitle_maker import SubtitleMaker
from modules.tts_engine import TTSEngine
from modules.merger import VideoMerger
import config


class TranslationPipeline:
    def __init__(self, output_dir=None):
        self.output_dir = Path(output_dir) or config.OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.downloader = BilibiliDownloader(self.output_dir)
        self.extractor = AudioExtractor()
        self.transcriber = Transcriber(model_size="base")
        self.translator = Translator()
        self.subtitle_maker = SubtitleMaker()
        self.tts_engine = TTSEngine()
        self.merger = VideoMerger()
        
        logger.info("✓ Translation pipeline initialized")

    def run_full_pipeline(self, video_url, source_lang, target_lang="vi", 
                         category="general", with_dubbing=False, subtitle_only=False):
        """
        Run complete translation pipeline
        
        Args:
            video_url (str): Bilibili video URL
            source_lang (str): Source language (zh, ja, ko, etc)
            target_lang (str): Target language (vi)
            category (str): Video category (movie, drama, comedy, general)
            with_dubbing (bool): Create dubbed version
            subtitle_only (bool): Only create subtitles
        
        Returns:
            dict: Output paths and results
        """
        try:
            logger.info("=" * 60)
            logger.info("🎬 Starting Translation Pipeline")
            logger.info("=" * 60)
            logger.info(f"URL: {video_url}")
            logger.info(f"Source: {source_lang} → Target: {target_lang}")
            logger.info(f"Category: {category}")
            logger.info(f"Dubbing: {with_dubbing} | Subtitle only: {subtitle_only}")
            
            results = {
                "video_url": video_url,
                "source_lang": source_lang,
                "target_lang": target_lang,
                "category": category,
                "outputs": {}
            }
            
            # Step 1: Download video
            logger.info("\n[1/7] Downloading video...")
            video_path = self.downloader.download(video_url, quality="720")
            results["outputs"]["video"] = str(video_path)
            
            # Step 2: Extract audio
            logger.info("\n[2/7] Extracting audio...")
            audio_path = self.extractor.extract(video_path)
            results["outputs"]["audio"] = str(audio_path)
            
            # Step 3: Transcribe audio
            logger.info("\n[3/7] Transcribing audio...")
            segments_original = self.transcriber.get_segments(audio_path, language=source_lang)
            results["outputs"]["transcription"] = segments_original
            
            # Step 4: Translate segments
            logger.info("\n[4/7] Translating segments...")
            segments_translated = []
            texts_to_translate = [seg['text'] for seg in segments_original]
            translated_texts = self.translator.translate_batch(
                texts_to_translate, 
                source_lang, 
                target_lang
            )
            
            for seg, trans_text in zip(segments_original, translated_texts):
                segments_translated.append({
                    'start': seg['start'],
                    'end': seg['end'],
                    'text': trans_text,
                    'original': seg['text']
                })
            
            results["outputs"]["translation"] = segments_translated
            
            # Step 5: Create subtitles
            logger.info("\n[5/7] Creating subtitles...")
            subtitle_path = self.subtitle_maker.create_srt(
                segments_translated,
                self.output_dir / f"subtitle_{target_lang}.srt"
            )
            results["outputs"]["subtitle"] = str(subtitle_path)
            
            # Step 6: Text-to-speech (if dubbing requested)
            dubbed_audio_path = None
            if with_dubbing:
                logger.info("\n[6/7] Generating dubbed audio...")
                texts_to_speak = [seg['text'] for seg in segments_translated]
                audio_files = self.tts_engine.synthesize_batch(
                    texts_to_speak,
                    language_code=target_lang,
                    output_dir=self.output_dir / "tts_temp"
                )
                logger.info(f"✓ Generated {len(audio_files)} audio files")
                results["outputs"]["tts_files"] = [str(f) for f in audio_files]
            else:
                logger.info("\n[6/7] Skipping TTS (dubbing not requested)")
            
            # Step 7: Merge video with subtitles/dubbing
            logger.info("\n[7/7] Finalizing output...")
            
            if not subtitle_only:
                # Add subtitle to video
                final_video = self.merger.add_subtitle_to_video(
                    video_path,
                    subtitle_path,
                    self.output_dir / f"video_with_subtitle.mp4"
                )
                results["outputs"]["final_video"] = str(final_video)
            
            logger.info("\n" + "=" * 60)
            logger.info("✓ Pipeline completed successfully!")
            logger.info("=" * 60)
            
            # Save results
            results_file = self.output_dir / "results.json"
            save_json(results, results_file)
            
            return results
        
        except Exception as e:
            logger.error(f"✗ Pipeline error: {e}")
            raise

    def run_subtitle_only(self, video_url, source_lang, target_lang="vi"):
        """
        Run pipeline with subtitles only (no dubbing)
        
        Args:
            video_url (str): Bilibili video URL
            source_lang (str): Source language
            target_lang (str): Target language
        
        Returns:
            dict: Results
        """
        return self.run_full_pipeline(
            video_url,
            source_lang,
            target_lang,
            subtitle_only=True,
            with_dubbing=False
        )

    def run_with_dubbing(self, video_url, source_lang, target_lang="vi", category="general"):
        """
        Run pipeline with dubbing
        
        Args:
            video_url (str): Bilibili video URL
            source_lang (str): Source language
            target_lang (str): Target language
            category (str): Video category
        
        Returns:
            dict: Results
        """
        return self.run_full_pipeline(
            video_url,
            source_lang,
            target_lang,
            category=category,
            with_dubbing=True,
            subtitle_only=False
        )


__all__ = ["TranslationPipeline"]
