# Use Python 3.11 as base image (compatible with the dependencies)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for some Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Gemini wrapper code and credentials
COPY Gemini_wrapper.py .
COPY nomnombox-8bf47.json .

# Set environment variables (if needed)
ENV PYTHONUNBUFFERED=1

# Expose the correct port (5009)
EXPOSE 5009

# Command to run the application
CMD ["python", "Gemini_wrapper.py"]
