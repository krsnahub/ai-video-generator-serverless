FROM runpod/base:0.4.0-cuda11.8.0

# Install dependencies
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Copy code
WORKDIR /app
COPY . /app

CMD ["python3", "-u", "handler.py"]
