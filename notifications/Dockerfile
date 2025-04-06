FROM python:3.12-slim-bookworm

WORKDIR /app

COPY requirements.txt .

# Install system dependencies required for some Python packages
RUN apt-get update && apt-get install -y gcc python3-dev && rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "notifications_consumer.py"]