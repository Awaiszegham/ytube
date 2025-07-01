from flask import Flask, request, jsonify
from flask_cors import CORS
from yt_dlp import YoutubeDL
import os
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use Railway's persistent storage if available, else local
DOWNLOAD_DIR = os.environ.get('RAILWAY_VOLUME_MOUNT_PATH', './videos')

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "YouTube Downloader API",
        "endpoints": {
            "POST /download": "Download a YouTube video",
            "GET /health": "Health check"
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "youtube-downloader"})

@app.route('/download', methods=['POST'])
def download_video():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        url = data.get("url")
        if not url:
            return jsonify({"error": "No URL provided"}), 400

        # Validate URL format
        if not (url.startswith('http://') or url.startswith('https://')):
            return jsonify({"error": "Invalid URL format"}), 400

        # Create download directory if missing
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        logger.info(f"Download directory: {DOWNLOAD_DIR}")
        
        ydl_opts = {
            'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'extractaudio': False,
            'audioformat': 'mp3',
            'embed_subs': True,
            'writesubtitles': False,
        }

        with YoutubeDL(ydl_opts) as ydl:
            logger.info(f"Extracting info for URL: {url}")
            info = ydl.extract_info(url, download=False)
            
            # Check if video is too long (optional safety check)
            duration = info.get('duration', 0)
            if duration > 3600:  # 1 hour limit
                return jsonify({"error": "Video too long (max 1 hour)"}), 400
            
            logger.info(f"Starting download for: {info.get('title', 'Unknown')}")
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        return jsonify({
            "title": info.get('title', 'Unknown'),
            "filename": os.path.basename(filename),
            "download_path": filename,
            "duration": info.get('duration', 0),
            "uploader": info.get('uploader', 'Unknown'),
            "status": "Downloaded successfully"
        })

    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        return jsonify({"error": f"Download failed: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") == "development"
    logger.info(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)

