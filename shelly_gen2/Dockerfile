FROM python:3.11-slim

# Install system packages
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy app and requirements
COPY app/ ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy start script
COPY run.sh /run.sh
RUN chmod +x /run.sh

# Environment for Ingress
ENV INGRESS_ENTRY /local
ENV LANG C.UTF-8

CMD [ "/run.sh" ]
