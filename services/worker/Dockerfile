FROM python:3.10-slim

WORKDIR /app

# Install system dependencies including redis-cli for debugging
RUN apt-get update && apt-get install -y \
    redis-tools \
    && rm -rf /var/lib/apt/lists/*

# Copy the entire services directory to maintain package structure
# Build context is set to ./services in docker-compose.yml
COPY . /app/services/

# Install Celery and message broker clients
RUN pip install --no-cache-dir celery redis pika


# Install PostgreSQL dependencies
RUN pip install --no-cache-dir sqlmodel psycopg2-binary alembic

# Install MongoDB dependencies (matching API versions)
RUN pip install --no-cache-dir beanie==1.25.0 motor==3.5.1 pymongo==4.8.0

# Set PYTHONPATH so 'services.worker' is importable
ENV PYTHONPATH=/app

WORKDIR /app/services/worker

CMD ["celery", "-A", "celery_app", "worker", "--loglevel=info"]
