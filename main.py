"""
Main CLI entry point for Video Translator Tool
"""
import click
from pathlib import Path
from modules.pipeline import TranslationPipeline
from utils.logger import logger
import config


@click.group()
def cli():
    """Video Translator Tool - Translate Bilibili videos to Vietnamese"""
    pass


@cli.command()
@click.option('--url', required=True, help='Bilibili video URL')
@click.option('--source-lang', default='zh', type=click.Choice(['zh', 'ja', 'ko']), 
              help='Source language (zh=Chinese, ja=Japanese, ko=Korean)')
@click.option('--output-lang', default='vi', help='Target language (default: vi=Vietnamese)')
@click.option('--category', default='general', 
              type=click.Choice(['movie', 'drama', 'comedy', 'anime', 'documentary', 'music', 'general']),
              help='Video category for translation style')
@click.option('--output-dir', default=None, help='Output directory')
@click.option('--subtitle-only', is_flag=True, help='Only create subtitles (no dubbing)')
@click.option('--with-dubbing', is_flag=True, help='Create dubbed audio and video')
def translate(url, source_lang, output_lang, category, output_dir, subtitle_only, with_dubbing):
    """
    Translate a Bilibili video
    
    Examples:
        # Create Vietnamese subtitles from Chinese video
        python main.py translate --url "https://www.bilibili.com/video/BV..." --source-lang zh --subtitle-only
        
        # Create dubbed Vietnamese version
        python main.py translate --url "https://www.bilibili.com/video/BV..." --source-lang ja --with-dubbing
    """
    try:
        output_dir = Path(output_dir) if output_dir else config.OUTPUT_DIR
        output_dir.mkdir(parents=True, exist_ok=True)
        
        pipeline = TranslationPipeline(output_dir)
        
        results = pipeline.run_full_pipeline(
            video_url=url,
            source_lang=source_lang,
            target_lang=output_lang,
            category=category,
            with_dubbing=with_dubbing,
            subtitle_only=subtitle_only
        )
        
        logger.info("\n📊 Results Summary:")
        logger.info(f"   Subtitle: {results['outputs'].get('subtitle', 'N/A')}")
        if results['outputs'].get('final_video'):
            logger.info(f"   Final Video: {results['outputs'].get('final_video', 'N/A')}")
        
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@cli.command()
@click.option('--url', required=True, help='Bilibili video URL')
@click.option('--source-lang', default='zh', type=click.Choice(['zh', 'ja', 'ko']), 
              help='Source language')
def subtitle(url, source_lang):
    """
    Create Vietnamese subtitles only
    
    Example:
        python main.py subtitle --url "https://www.bilibili.com/video/BV..." --source-lang zh
    """
    try:
        pipeline = TranslationPipeline()
        results = pipeline.run_subtitle_only(url, source_lang)
        logger.info(f"\n✓ Subtitle created: {results['outputs']['subtitle']}")
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@cli.command()
@click.option('--url', required=True, help='Bilibili video URL')
@click.option('--source-lang', default='zh', type=click.Choice(['zh', 'ja', 'ko']), 
              help='Source language')
@click.option('--category', default='general', 
              type=click.Choice(['movie', 'drama', 'comedy', 'anime', 'documentary', 'music', 'general']),
              help='Video category')
def dub(url, source_lang, category):
    """
    Create dubbed Vietnamese video
    
    Example:
        python main.py dub --url "https://www.bilibili.com/video/BV..." --source-lang ja --category anime
    """
    try:
        pipeline = TranslationPipeline()
        results = pipeline.run_with_dubbing(url, source_lang, category=category)
        logger.info(f"\n✓ Dubbed video created: {results['outputs'].get('final_video', 'N/A')}")
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@cli.command()
def info():
    """Show tool information and system configuration"""
    click.echo("\n" + "=" * 60)
    click.echo("Video Translator Tool")
    click.echo("=" * 60)
    click.echo(f"\nSupported Languages:")
    for lang_code, lang_name in config.LANGUAGE_MAP.items():
        click.echo(f"  {lang_code:6} → {lang_name}")
    
    click.echo(f"\nSupported Categories:")
    for cat_code, cat_name in config.CATEGORIES.items():
        click.echo(f"  {cat_code:12} → {cat_name}")
    
    click.echo(f"\nConfiguration:")
    click.echo(f"  Output Directory: {config.OUTPUT_DIR}")
    click.echo(f"  Whisper Model: {config.DEFAULT_WHISPER_MODEL}")
    click.echo(f"  Default Quality: {config.DEFAULT_VIDEO_QUALITY}p")
    click.echo(f"  Audio Sample Rate: {config.AUDIO_SAMPLE_RATE} Hz")
    click.echo("\n" + "=" * 60 + "\n")


if __name__ == '__main__':
    cli()
