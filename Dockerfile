# Base image (Python 3.9)
FROM python:3.9-slim

# Install FFmpeg and clean up
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies first (caching optimization)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose port (matches Railway's public networking port)
EXPOSE 8080

# Run the app - CHANGE "app.main" to your actual Python module and app variable
# Example: If your app is defined in main.py as `app = Flask(__name__)`, use "main:app"
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--timeout", "120"]
