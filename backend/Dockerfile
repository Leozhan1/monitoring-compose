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

RUN pip install -r requirements.txt
RUN pip install docker psutil

# Expose your API port (change if your API uses a different port)
EXPOSE 5000

# Command to start the API
CMD ["python", "app.py"]
#CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]