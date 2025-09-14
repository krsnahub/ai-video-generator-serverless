# AI Video Generator - RunPod Serverless Dockerfile
# Base image with CUDA support
FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04

# Set working directory
WORKDIR /

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libglib2.0-0 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Clone ComfyUI
RUN git clone https://github.com/comfyanonymous/ComfyUI.git
WORKDIR /ComfyUI

# Install ComfyUI dependencies
RUN pip install -r requirements.txt

# Install additional dependencies for video processing
RUN pip install opencv-python imageio[ffmpeg] av

# Install custom nodes for video generation
WORKDIR /ComfyUI/custom_nodes

# VideoHelperSuite for video processing
RUN git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite.git
WORKDIR /ComfyUI/custom_nodes/ComfyUI-VideoHelperSuite
RUN pip install -r requirements.txt

# AnimateDiff support (for future models)
WORKDIR /ComfyUI/custom_nodes
RUN git clone https://github.com/ArtVentureX/comfyui-animatediff.git
WORKDIR /ComfyUI/custom_nodes/comfyui-animatediff
RUN pip install -r requirements.txt

# Install RunPod serverless
RUN pip install runpod

# Create required directories
RUN mkdir -p /ComfyUI/models/checkpoints \
    /ComfyUI/models/vae \
    /ComfyUI/models/text_encoders \
    /ComfyUI/models/clip \
    /ComfyUI/input \
    /ComfyUI/output

# Download Wan 2.2 models (commented out - too large for build)
# Uncomment these lines if you want models baked into the image
# WORKDIR /ComfyUI/models

# # Wan 2.2 Models
# RUN wget -P checkpoints/ https://huggingface.co/Wan-AI/Wan2.2-T2V-A14B/resolve/main/wan2.2_diffusion_transformer.safetensors
# RUN wget -P checkpoints/ https://huggingface.co/Wan-AI/Wan2.2-I2V-A14B/resolve/main/wan2.2_i2v_diffusion_transformer.safetensors
# RUN wget -P vae/ https://huggingface.co/Wan-AI/Wan2.2-T2V-A14B/resolve/main/wan2.2_vae.safetensors
# RUN wget -P text_encoders/ https://huggingface.co/Wan-AI/Wan2.2-T2V-A14B/resolve/main/t5xxl_fp16.safetensors

# Copy serverless handler
WORKDIR /
COPY handler.py /handler.py
COPY requirements.txt /requirements.txt

# Install handler dependencies
RUN pip install -r /requirements.txt

# Set environment variables
ENV PYTHONPATH="/ComfyUI"
ENV COMFYUI_PATH="/ComfyUI"

# Create startup script
RUN echo '#!/bin/bash\n\
echo "🚀 AI Video Generator - Starting..."\n\
echo "💾 Available models in /ComfyUI/models/"\n\
ls -la /ComfyUI/models/checkpoints/ || echo "⚠️  No checkpoints found - models will be downloaded on first use"\n\
echo "🎬 Starting serverless handler..."\n\
python /handler.py' > /start.sh

RUN chmod +x /start.sh

# Expose ComfyUI port (for internal use)
EXPOSE 8188

# Start the serverless handler
CMD ["/start.sh"]
