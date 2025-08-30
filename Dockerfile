FROM python:3.10-slim

WORKDIR /app

# Install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add code
COPY handler.py .

CMD ["python", "-u", "handler.py"]
