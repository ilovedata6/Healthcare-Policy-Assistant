# Use official Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install system packages and Python dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential poppler-utils && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy app source
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Expose Streamlit's default port
EXPOSE 8501

# Run Streamlit
CMD ["python", "run.py"]
