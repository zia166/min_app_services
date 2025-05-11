# Use official Python runtime as a parent image
FROM python:3.11.1

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /var/www/webapp

# Install system dependencies (if needed for packages like pymongo, boto3, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies in one layer for better caching
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Then copy the rest of the application
COPY . .

# Expose Django's default port
EXPOSE 8000

# Default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
