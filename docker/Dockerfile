# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements/base.txt requirements/prod.txt ./
RUN pip install --user --no-cache-dir -r base.txt -r prod.txt

# Stage 2: Runtime
FROM python:3.11-slim as runtime

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user
RUN useradd --create-home --shell /bin/bash app

# Copy Python packages from builder
COPY --from=builder /root/.local /home/app/.local
ENV PATH=/home/app/.local/bin:$PATH

# Copy application code
COPY --chown=app:app src/ ./src/

# Set environment
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Switch to non-root user
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
