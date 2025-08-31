FROM ubuntu:22.04

# Install Python and ffmpeg
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    ffmpeg \
    libavcodec-extra \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set Python as default
RUN ln -s /usr/bin/python3.10 /usr/bin/python

WORKDIR /app

# Install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add code
COPY handler.py .

CMD ["python", "-u", "handler.py"]
