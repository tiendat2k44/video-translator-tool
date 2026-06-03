"""
Flask Web UI for Video Translator Tool
"""
from flask import Flask, render_template, request, jsonify, send_file
from pathlib import Path
import json
import os
from datetime import datetime
from modules.pipeline import TranslationPipeline
from utils.logger import logger
import config

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max upload
app.config['UPLOAD_FOLDER'] = config.OUTPUT_DIR

# Store job status
jobs = {}


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/api/languages', methods=['GET'])
def get_languages():
    """Get supported languages"""
    return jsonify({
        'success': True,
        'languages': config.LANGUAGE_MAP,
        'language_codes': config.LANGUAGE_CODES
    })


@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get supported categories"""
    return jsonify({
        'success': True,
        'categories': config.CATEGORIES
    })


@app.route('/api/translate', methods=['POST'])
def translate_video():
    """Translate video"""
    try:
        data = request.get_json()
        
        # Validate input
        video_url = data.get('video_url', '').strip()
        source_lang = data.get('source_lang', 'zh')
        target_lang = data.get('target_lang', 'vi')
        category = data.get('category', 'general')
        mode = data.get('mode', 'subtitle')  # subtitle or dubbing
        
        if not video_url:
            return jsonify({'success': False, 'error': 'Video URL required'}), 400
        
        # Create job ID
        job_id = f"job_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        output_dir = config.OUTPUT_DIR / job_id
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Store job info
        jobs[job_id] = {
            'id': job_id,
            'video_url': video_url,
            'source_lang': source_lang,
            'target_lang': target_lang,
            'category': category,
            'mode': mode,
            'status': 'processing',
            'progress': 0,
            'created_at': datetime.now().isoformat(),
            'output_dir': str(output_dir)
        }
        
        # Run translation
        pipeline = TranslationPipeline(output_dir)
        
        if mode == 'dubbing':
            results = pipeline.run_with_dubbing(
                video_url=video_url,
                source_lang=source_lang,
                target_lang=target_lang,
                category=category
            )
        else:  # subtitle only
            results = pipeline.run_subtitle_only(
                video_url=video_url,
                source_lang=source_lang,
                target_lang=target_lang
            )
        
        # Update job status
        jobs[job_id]['status'] = 'completed'
        jobs[job_id]['progress'] = 100
        jobs[job_id]['results'] = results['outputs']
        
        logger.info(f"✓ Job {job_id} completed")
        
        return jsonify({
            'success': True,
            'job_id': job_id,
            'results': results['outputs']
        })
    
    except Exception as e:
        logger.error(f"✗ Translation error: {e}")
        if 'job_id' in locals():
            jobs[job_id]['status'] = 'error'
            jobs[job_id]['error'] = str(e)
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/job/<job_id>', methods=['GET'])
def get_job_status(job_id):
    """Get job status"""
    if job_id not in jobs:
        return jsonify({'success': False, 'error': 'Job not found'}), 404
    
    return jsonify({
        'success': True,
        'job': jobs[job_id]
    })


@app.route('/api/jobs', methods=['GET'])
def list_jobs():
    """List all jobs"""
    return jsonify({
        'success': True,
        'jobs': list(jobs.values())
    })


@app.route('/api/download/<job_id>/<file_type>', methods=['GET'])
def download_file(job_id, file_type):
    """Download output file"""
    if job_id not in jobs:
        return jsonify({'success': False, 'error': 'Job not found'}), 404
    
    job = jobs[job_id]
    output_dir = Path(job['output_dir'])
    
    # Map file types to actual files
    file_mapping = {
        'subtitle': 'subtitle_vi.srt',
        'video': 'video_with_subtitle.mp4',
        'dubbed_video': 'video_vi_dubbed_final.mp4',
        'transcription': 'transcription.json',
        'results': 'results.json'
    }
    
    if file_type not in file_mapping:
        return jsonify({'success': False, 'error': 'Invalid file type'}), 400
    
    file_path = output_dir / file_mapping[file_type]
    
    if not file_path.exists():
        return jsonify({'success': False, 'error': 'File not found'}), 404
    
    return send_file(
        file_path,
        as_attachment=True,
        download_name=file_path.name
    )


@app.route('/api/settings', methods=['GET'])
def get_settings():
    """Get application settings"""
    return jsonify({
        'success': True,
        'settings': {
            'output_dir': str(config.OUTPUT_DIR),
            'whisper_model': config.DEFAULT_WHISPER_MODEL,
            'video_quality': config.DEFAULT_VIDEO_QUALITY,
            'audio_sample_rate': config.AUDIO_SAMPLE_RATE
        }
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'running',
        'timestamp': datetime.now().isoformat()
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'success': False, 'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Server error: {error}")
    return jsonify({'success': False, 'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
