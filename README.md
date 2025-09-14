# 🎬 AI Video Generator - Serverless

Universal AI video generation with RunPod serverless integration. Supports multiple video models with pay-per-request pricing.

## 🚀 Supported Models

### Currently Available
- **Wan 2.2 T2V** - Text-to-Video (14B parameters)
- **Wan 2.2 I2V** - Image-to-Video (14B parameters)

### Coming Soon
- **Mochi** - High-quality video generation
- **LTX Video** - Fast video synthesis
- **Kling** - Advanced video AI
- **Custom models** - Easy to add new models

## 💰 Cost Efficiency

- **Pay per request** - No idle costs
- **~1-5 cents per video** - Extremely cost effective
- **Auto-scaling** - Handles traffic spikes automatically
- **Zero infrastructure** - No servers to manage

## 🎯 Quick Start

### 1. Deploy to RunPod

```bash
# Clone this repo
git clone https://github.com/yourusername/ai-video-generator-serverless.git

# Deploy to RunPod Serverless
# Use this repo URL in RunPod Hub
```

### 2. API Usage

```python
import requests

# Your RunPod endpoint
endpoint = "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID"
headers = {"Authorization": "Bearer YOUR_API_KEY"}

# Text-to-Video generation
payload = {
    "input": {
        "model_type": "wan22_t2v",
        "prompt": "A beautiful sunset over mountains with gentle clouds",
        "negative_prompt": "blurry, low quality, distorted",
        "width": 1280,
        "height": 720,
        "steps": 30,
        "cfg": 7.5,
        "seed": -1
    }
}

response = requests.post(f"{endpoint}/run", json=payload, headers=headers)
job_id = response.json()["id"]

# Check status
status_response = requests.get(f"{endpoint}/status/{job_id}", headers=headers)
```

### 3. Image-to-Video

```python
# Convert image to base64
import base64
with open("input_image.jpg", "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode()

# I2V generation
payload = {
    "input": {
        "model_type": "wan22_i2v",
        "prompt": "The image comes to life with gentle movement",
        "image_data": f"data:image/jpeg;base64,{image_base64}",
        "strength": 0.8,
        "steps": 30
    }
}
```

## ⚙️ Configuration Options

### Text-to-Video Parameters
- `prompt` (string) - Description of the video to generate
- `negative_prompt` (string) - What to avoid in the video
- `width` (int) - Video width (default: 1280)
- `height` (int) - Video height (default: 720)
- `steps` (int) - Generation steps (default: 30)
- `cfg` (float) - CFG scale (default: 7.5)
- `seed` (int) - Random seed (-1 for random)

### Image-to-Video Parameters
- `image_data` (string) - Base64 encoded input image
- `strength` (float) - How much to change the image (default: 0.8)
- All T2V parameters also apply

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Your Flask    │───▶│   RunPod API     │───▶│   Serverless    │
│   Frontend      │    │   Endpoint       │    │   Container     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
                                               ┌─────────────────┐
                                               │   ComfyUI +     │
                                               │   Video Models  │
                                               └─────────────────┘
```

## 🚀 Deployment Guide

### Option 1: RunPod Hub Integration
1. Push this repo to GitHub
2. Add repo to RunPod Hub
3. Deploy as serverless endpoint
4. Use endpoint URL in your applications

### Option 2: Manual Docker Build
```bash
# Build container
docker build -t ai-video-generator .

# Push to container registry
docker push your-registry/ai-video-generator

# Deploy to RunPod using custom container
```

## 🎛️ Advanced Features

### Model Management
- **Automatic model loading** - Models downloaded on first use
- **Smart caching** - Models cached between requests
- **Multi-model support** - Easy to add new models

### Cost Optimization
- **Efficient scaling** - Scales to zero when idle
- **Batch processing** - Handle multiple requests efficiently  
- **Resource optimization** - Minimal memory footprint

### Monitoring
- **Detailed logging** - Track generation progress
- **Error handling** - Graceful failure recovery
- **Performance metrics** - Monitor costs and speed

## 🛠️ Local Development

```bash
# Clone repo
git clone https://github.com/yourusername/ai-video-generator-serverless.git
cd ai-video-generator-serverless

# Install dependencies
pip install -r requirements.txt

# Set up ComfyUI (for local testing)
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI && pip install -r requirements.txt

# Test handler locally
python handler.py
```

## 📊 Performance Benchmarks

| Model | Resolution | Duration | Generation Time | Cost |
|-------|------------|----------|-----------------|------|
| Wan 2.2 T2V | 1280x720 | 5s | ~2-3 minutes | ~$0.03 |
| Wan 2.2 I2V | 1280x720 | 5s | ~2-4 minutes | ~$0.04 |
| Wan 2.2 T2V | 832x480 | 5s | ~1-2 minutes | ~$0.02 |

## 🐛 Troubleshooting

### Common Issues

**"Model not found" error**
- Models are downloaded on first use
- Ensure sufficient container disk space (20GB+)
- Check model URLs in handler.py

**Generation timeout**
- Increase timeout in RunPod settings (600s recommended)
- Try smaller resolution for faster generation
- Check GPU availability

**Out of memory**
- Use smaller model variants
- Reduce batch size
- Enable model offloading

### Debug Mode
```python
# Add to your request payload
"input": {
    "debug": True,
    # ... other parameters
}
```

## 🤝 Contributing

### Adding New Models
1. Create model workflow function in `handler.py`
2. Add model download URLs in `Dockerfile`
3. Update README with model info
4. Test thoroughly before merging

### Model Integration Template
```python
def create_new_model_workflow(prompt, **kwargs):
    """Create workflow for new model"""
    return {
        # ComfyUI workflow definition
    }
```

## 📄 License

Private use only. Contact owner for commercial licensing.

## 🆘 Support

For issues and questions:
1. Check troubleshooting section
2. Review RunPod logs
3. Test with simpler prompts
4. Contact via GitHub issues

## 🔗 Useful Links

- [RunPod Documentation](https://docs.runpod.io/)
- [ComfyUI GitHub](https://github.com/comfyanonymous/ComfyUI)
- [Wan Models](https://huggingface.co/Wan-AI)
- [Cost Calculator](https://runpod.io/pricing)

---

**Ready to generate amazing AI videos!** 🎬✨
