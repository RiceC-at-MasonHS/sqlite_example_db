FROM python:3.13-slim

WORKDIR /app

# Install sqlite3 CLI directly
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

COPY db_tool.py .

# Create data directory mount point
RUN mkdir -p /data

# Default command to keep container alive for interactive use
CMD ["tail", "-f", "/dev/null"]
