# Use Python base image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose your API port (change if your API uses a different port)
EXPOSE 5000

# Command to start the API
CMD ["python", "main.py"]
