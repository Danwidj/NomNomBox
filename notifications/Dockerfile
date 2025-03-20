FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default to running the API, but can be overridden
CMD ["python", "notifications_service.py"]
