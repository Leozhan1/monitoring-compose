FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
Run pip install docker psutil

COPY . .

EXPOSE 8000

#CMD ["sh", "-c", "cd /app && gunicorn -b 0.0.0.0:8000 front:app"]
CMD ["python", "front.py"]
