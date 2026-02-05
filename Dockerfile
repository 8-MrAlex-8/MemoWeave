# Use a lightweight Python base image
FROM python:3.10-slim

# Set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies (needed for some python packages like gcc for compilation)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements keys
COPY requirements.txt .

# Install dependencies
# We use --no-cache-dir to keep the image small
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    python -m spacy download en_core_web_sm

# Copy the rest of the application
COPY . .

# Make the startup script executable
RUN chmod +x start.sh

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
# Use startup script for proper environment variable handling
CMD ["./start.sh"]
