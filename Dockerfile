
FROM python:3.12-slim-bookworm

WORKDIR /app

# Install system libraries required by MediaPipe
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgles2 \
    libegl1 \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --no-input

# Start Django application
CMD ["sh", "-c", "python manage.py migrate && python manage.py seed_hairstyles && gunicorn facesite.wsgi:application --bind 0.0.0.0:${PORT:-10000}"]
