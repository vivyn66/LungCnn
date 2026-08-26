# Use official Python 3.7 slim image
FROM python:3.7-slim

# Install system dependencies needed for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port
EXPOSE 5000

# Set environment variables (should be overridden in production)
ENV PORT=5000

# Run the app via wsgi production server
CMD ["python", "wsgi.py"]
