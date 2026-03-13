# Dockerfile for Iran Cities API Server
FROM python:3.9-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY iran_cities.json .
COPY api_server.py .

# Expose port
EXPOSE 8000

# Set environment variables
ENV FLASK_APP=api_server.py
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "api_server.py"]
