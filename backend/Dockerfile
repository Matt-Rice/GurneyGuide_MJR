# Use a minimal Python base image
FROM python:3.9-slim

# Expose port 8000 for the FastAPI service
EXPOSE 8000

# Environment variables for cleaner output & better performance
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN python -m pip install --no-cache-dir --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Start Gunicorn with UvicornWorker
CMD ["gunicorn", "--workers", "1", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "app.main:app"]
