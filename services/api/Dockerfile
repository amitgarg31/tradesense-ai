# Use a lightweight Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Upgrade pip and clean cache
RUN pip install --upgrade pip

# Copy dependency files first
COPY requirements.txt /app/requirements.txt

# Force clean reinstall of all dependencies to avoid cached PyMongo
RUN pip install --no-cache-dir --force-reinstall \
    beanie==1.25.0 \
    motor==3.5.1 \
    pymongo==4.8.0 && \
    pip install --no-cache-dir -r /app/requirements.txt && \
    pip install --no-cache-dir sqlmodel psycopg2-binary alembic

# Copy the source code to match worker structure
COPY . /app/services/api/

# Set PYTHONPATH so 'services.api' is importable
ENV PYTHONPATH=/app

# Set working directory to api folder
WORKDIR /app/services/api

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
