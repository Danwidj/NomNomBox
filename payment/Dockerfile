# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

ARG INSTALL_BUILD_DEPS
RUN eval "$INSTALL_BUILD_DEPS"

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose the port your app runs on
EXPOSE 5004

# Run the Flask app
CMD ["python", "payment.py"]
