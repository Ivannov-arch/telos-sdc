# Production-ready Dockerfile for Telos / Aiversecity Backend
# Python 3.11 slim base image for minimal footprint and security
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    PORT=8000

# Set working directory inside container
WORKDIR /app

# Install system dependencies (curl for container health checks)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first (leveraging Docker layer caching)
COPY src/backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy application source code
COPY src /app/src

# Set working directory to src for running uvicorn
WORKDIR /app/src

# Expose default port (Render / Cloud Run will inject $PORT dynamically)
EXPOSE 8000

# Health check to ensure service is responding
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Start Uvicorn server, supporting dynamic $PORT from cloud environments
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT}"]
