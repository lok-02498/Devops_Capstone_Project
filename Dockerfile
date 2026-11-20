# ==========================================
# Stage 1: Build Dependencies
# ==========================================
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ==========================================
# Stage 2: Production Distroless/Minimal Runtime
# ==========================================
FROM python:3.11-slim AS runner

# Security: Run as non-root user
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /bin/sh -m appuser

WORKDIR /app

# Copy installed python dependencies from builder
COPY --from=builder /install /usr/local

# Copy application source code
COPY app/ /app/

# Set correct ownership for non-root user
RUN chown -R appuser:appgroup /app

USER 10001:10001

ENV PYTHONUNBUFFERED=1 \
    PORT=5000 \
    APP_ENV=production \
    APP_VERSION=v1.0.0

EXPOSE 5000

# Docker native health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health/live')" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", "main:app"]
