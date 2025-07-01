# YouTube Downloader API

A Flask-based REST API for downloading YouTube videos using yt-dlp.

## Deployment

**Live URL:** https://e5h6i7c09zw8.manus.space

## API Endpoints

### GET /
Returns API information and available endpoints.

**Response:**
```json
{
  "message": "YouTube Downloader API",
  "endpoints": {
    "POST /download": "Download a YouTube video",
    "GET /health": "Health check"
  }
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "youtube-downloader"
}
```

### POST /download
Downloads a YouTube video.

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Response (Success):**
```json
{
  "title": "Video Title",
  "filename": "video_file.mp4",
  "download_path": "/path/to/video_file.mp4",
  "duration": 300,
  "uploader": "Channel Name",
  "status": "Downloaded successfully"
}
```

**Response (Error):**
```json
{
  "error": "Error message"
}
```

## Features

- Downloads YouTube videos in best available quality
- Supports MP4 format with audio
- CORS enabled for cross-origin requests
- Error handling and validation
- Video duration limit (1 hour max)
- Persistent storage support for Railway deployment

## Technical Details

- **Framework:** Flask 3.0.2
- **Video Downloader:** yt-dlp (latest version)
- **CORS Support:** Flask-CORS 4.0.0
- **Production Server:** Gunicorn 21.2.0
- **Python Version:** 3.11

## Environment Variables

- `PORT`: Server port (default: 5000)
- `RAILWAY_VOLUME_MOUNT_PATH`: Persistent storage path for downloads
- `FLASK_ENV`: Environment mode (development/production)

## Local Development

1. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## Deployment

The application is configured for deployment on Railway with:
- Procfile for Gunicorn configuration
- Runtime specification (Python 3.11)
- Environment variable support
- Persistent storage integration

## Usage Example

```bash
# Health check
curl https://e5h6i7c09zw8.manus.space/health

# Download a video
curl -X POST https://e5h6i7c09zw8.manus.space/download \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

## Error Handling

The API includes comprehensive error handling for:
- Invalid or missing URLs
- Network connectivity issues
- Video processing errors
- File system errors
- Video duration limits

All errors return appropriate HTTP status codes and descriptive error messages.

