# Stage 1: Build
FROM python:3.10-slim as builder

# Install only essential build deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc python3-dev libportaudio2 portaudio19-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

# Create lean virtual environment
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.10-slim

# Install only runtime deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    libportaudio2 ffmpeg libsndfile1 && \
    rm -rf /var/lib/apt/lists/*

# Copy only what's needed from builder
COPY --from=builder /opt/venv /opt/venv

# Create non-root user
RUN useradd -m appuser && mkdir /app && chown appuser:appuser /app

WORKDIR /app
USER appuser

# Copy application files (respects .dockerignore)
COPY --chown=appuser:appuser . .

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

EXPOSE 5000
CMD ["python", "app.py"]