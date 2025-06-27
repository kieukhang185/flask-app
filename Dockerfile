FROM python:3.9-slim

WORKDIR /app

# ensure apt-cache is fresh, install netcat, clean up
RUN apt-get update \
 && apt-get install -y --no-install-recommends netcat-openbsd  \
 && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

ENTRYPOINT ["sh", "/app/entrypoint.sh"]