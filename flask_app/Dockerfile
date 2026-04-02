FROM python:3.13-slim

WORKDIR /app

# Install system dependencies if needed (sqlite3 for manual check)
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure data directory exists
RUN mkdir -p /data

EXPOSE 5000

CMD ["python", "app.py"]
