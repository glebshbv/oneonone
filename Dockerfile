# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables to prevent .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install ffmpeg and other dependencies
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Create a directory for the app
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Install Alembic
RUN pip install alembic

# Copy the FastAPI app code
COPY . /app/

# Expose the port FastAPI is running on
EXPOSE 8000

# Run Alembic migrations and then the FastAPI app
CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]
