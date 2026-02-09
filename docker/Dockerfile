# Use official Python slim image
FROM python:3.10-slim

# 1. Update OS packages to latest versions (fix vulnerabilities)
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 2. Set working directory
WORKDIR /app

# 3. Copy application files
COPY app/ .

# 4. Upgrade pip & install Python dependencies
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. Expose port and start the app
EXPOSE 5000
CMD ["python", "app.py"]

