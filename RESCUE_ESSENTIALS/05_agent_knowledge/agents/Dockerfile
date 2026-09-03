FROM python:3.11-slim

WORKDIR /app

# System deps for chromadb, snscrape, tesseract, and other native extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    tesseract-ocr \
    && pip install --no-cache-dir snscrape \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy agent system
COPY htc_agents/ ./htc_agents/

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8067/health || exit 1

EXPOSE 8067

CMD ["python", "-m", "htc_agents"]
