#!/usr/bin/env python3
"""
AI Video Generator - RunPod Serverless Handler
Supports: Wan 2.2, Wan 2.1, Mochi, LTX Video (future)
"""

import runpod
import json
import base64
import io
import os
import subprocess
import time
import requests
from PIL import Image
import torch

# Global variables for model management
loaded_models = {}
comfyui_process = None

def start_comfyui():
    """Start ComfyUI server if not running"""
    global comfyui_process
    
    if comfyui_process is None:
        print("🚀 Starting ComfyUI server...")
        cmd = [
            "python", "/ComfyUI/main.py",
            "--listen", "0.0.0.0",
            "--port", "8188",
            "--dont-print-server"
        ]
        comfyui_process = subprocess.Popen(cmd, cwd="/ComfyUI")
        
        # Wait for ComfyUI to be ready
        for i in range(60):  # 60 second timeout
            try:
                response = requests.get("http://localhost:8188", timeout=2)
                if response.status_code == 200:
                    print("✅ ComfyUI server ready!")
                    return True
            except:
                time.sleep(1)
        
        print("❌ ComfyUI failed to start")
        return False
    return True

def create_wan22_t2v_workflow(prompt, negative_prompt="", width=1280, height=720, steps=30, cfg=7.5, seed=-1):
    """Create Wan 2.2 Text-to-Video workflow"""
    if seed == -1:
        seed = int(time.time())
    
    return {
        "1": {
            "inputs": {
                "text": prompt,
                "clip": ["4", 1]
            },
            "class_type": "CLIPTextEncode"
        },
        "2": {
            "inputs": {
                "text": negative_prompt,
                "clip": ["4", 1]
            },
            "class_type": "CLIPTextEncode"
        },
        "3": {
            "inputs": {
                "width": width,
                "height": height,
                "batch_size": 1
            },
            "class_type": "EmptyLatentImage"
        },
        "4": {
            "inputs": {
                "clip_name": "t5xxl_fp16.safetensors"
            },
            "class_type": "CLIPLoader"
        },
        "5": {
            "inputs": {
                "unet_name": "wan2.2_diffusion_transformer.safetensors"
            },
            "class_type": "UNETLoader"
        },
        "6": {
            "inputs": {
                "seed": seed,
                "steps": steps,
                "cfg": cfg,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 1.0,
                "model": ["5", 0],
                "positive": ["1", 0],
                "negative": ["2", 0],
                "latent_image": ["3", 0]
            },
            "class_type": "KSampler"
        },
        "7": {
            "inputs": {
                "vae_name": "wan2.2_vae.safetensors"
            },
            "class_type": "VAELoader"
        },
        "8": {
            "inputs": {
                "samples": ["6", 0],
                "vae": ["7", 0]
            },
            "class_type": "VAEDecode"
        },
        "9": {
            "inputs": {
                "filename_prefix": "wan22_video_",
                "fps": 24,
                "format": "video/mp4",
                "images": ["8", 0]
            },
            "class_type": "VHS_VideoCombine"
        }
    }

def create_wan22_i2v_workflow(prompt, image_base64, negative_prompt="", width=1280, height=720, steps=30, cfg=7.5, seed=-1, strength=0.8):
    """Create Wan 2.2 Image-to-Video workflow"""
    if seed == -1:
        seed = int(time.time())
    
    # Save image for ComfyUI
    image_data = base64.b64decode(image_base64.split(',')[1] if ',' in image_base64 else image_base64)
    image = Image.open(io.BytesIO(image_data))
    image_path = f"/ComfyUI/input/input_{int(time.time())}.png"
    image.save(image_path)
    
    return {
        "1": {
            "inputs": {
                "image": os.path.basename(image_path),
                "upload": "image"
            },
            "class_type": "LoadImage"
        },
        "2": {
            "inputs": {
                "text": prompt,
                "clip": ["5", 1]
            },
            "class_type": "CLIPTextEncode"
        },
        "3": {
            "inputs": {
                "text": negative_prompt,
                "clip": ["5", 1]
            },
            "class_type": "CLIPTextEncode"
        },
        "4": {
            "inputs": {
                "pixels": ["1", 0],
                "vae": ["8", 0]
            },
            "class_type": "VAEEncode"
        },
        "5": {
            "inputs": {
                "clip_name": "t5xxl_fp16.safetensors"
            },
            "class_type": "CLIPLoader"
        },
        "6": {
            "inputs": {
                "unet_name": "wan2.2_i2v_diffusion_transformer.safetensors"
            },
            "class_type": "UNETLoader"
        },
        "7": {
            "inputs": {
                "seed": seed,
                "steps": steps,
                "cfg": cfg,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": strength,
                "model": ["6", 0],
                "positive": ["2", 0],
                "negative": ["3", 0],
                "latent_image": ["4", 0]
            },
            "class_type": "KSampler"
        },
        "8": {
            "inputs": {
                "vae_name": "wan2.2_vae.safetensors"
            },
            "class_type": "VAELoader"
        },
        "9": {
            "inputs": {
                "samples": ["7", 0],
                "vae": ["8", 0]
            },
            "class_type": "VAEDecode"
        },
        "10": {
            "inputs": {
                "filename_prefix": "wan22_i2v_",
                "fps": 24,
                "format": "video/mp4",
                "images": ["9", 0]
            },
            "class_type": "VHS_VideoCombine"
        }
    }

def queue_comfyui_prompt(workflow):
    """Submit workflow to ComfyUI and wait for completion"""
    try:
        # Submit prompt
        response = requests.post("http://localhost:8188/prompt", json={"prompt": workflow})
        if response.status_code != 200:
            return {"error": f"Failed to submit prompt: {response.text}"}
        
        result = response.json()
        prompt_id = result.get("prompt_id")
        
        if not prompt_id:
            return {"error": "No prompt ID returned"}
        
        print(f"📋 Submitted prompt: {prompt_id}")
        
        # Wait for completion
        max_wait = 600  # 10 minutes
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            # Check history
            history_response = requests.get(f"http://localhost:8188/history/{prompt_id}")
            
            if history_response.status_code == 200:
                history = history_response.json()
                
                if prompt_id in history:
                    outputs = history[prompt_id].get("outputs", {})
                    
                    # Look for video output
                    for node_id, output in outputs.items():
                        if "gifs" in output and output["gifs"]:
                            video_info = output["gifs"][0]
                            
                            # Get video file
                            video_response = requests.get(
                                f"http://localhost:8188/view", 
                                params={
                                    "filename": video_info["filename"],
                                    "subfolder": video_info.get("subfolder", ""),
                                    "type": "output"
                                }
                            )
                            
                            if video_response.status_code == 200:
                                # Convert to base64
                                video_base64 = base64.b64encode(video_response.content).decode()
                                
                                return {
                                    "success": True,
                                    "video_base64": video_base64,
                                    "filename": video_info["filename"]
                                }
            
            time.sleep(2)  # Wait 2 seconds before checking again
        
        return {"error": "Generation timeout"}
        
    except Exception as e:
        return {"error": f"ComfyUI error: {str(e)}"}

def handler(job):
    """Main RunPod handler function"""
    try:
        # Get job input
        job_input = job["input"]
        
        # Validate required fields
        model_type = job_input.get("model_type", "wan22_t2v")
        prompt = job_input.get("prompt", "")
        
        if not prompt:
            return {"error": "Prompt is required"}
        
        # Start ComfyUI if needed
        if not start_comfyui():
            return {"error": "Failed to start ComfyUI"}
        
        # Extract parameters
        negative_prompt = job_input.get("negative_prompt", "blurry, low quality, distorted")
        width = job_input.get("width", 1280)
        height = job_input.get("height", 720)
        steps = job_input.get("steps", 30)
        cfg = job_input.get("cfg", 7.5)
        seed = job_input.get("seed", -1)
        strength = job_input.get("strength", 0.8)
        
        print(f"🎬 Generating {model_type} video...")
        print(f"📝 Prompt: {prompt[:100]}...")
        
        # Create workflow based on model type
        if model_type == "wan22_t2v":
            workflow = create_wan22_t2v_workflow(
                prompt, negative_prompt, width, height, steps, cfg, seed
            )
        elif model_type == "wan22_i2v":
            image_data = job_input.get("image_data")
            if not image_data:
                return {"error": "Image data required for I2V generation"}
            
            workflow = create_wan22_i2v_workflow(
                prompt, image_data, negative_prompt, width, height, steps, cfg, seed, strength
            )
        else:
            return {"error": f"Unsupported model type: {model_type}"}
        
        # Generate video
        result = queue_comfyui_prompt(workflow)
        
        if "error" in result:
            return result
        
        print("✅ Video generation completed!")
        
        return {
            "images": [{
                "data": result["video_base64"],
                "type": "base64",
                "filename": result["filename"]
            }]
        }
        
    except Exception as e:
        print(f"❌ Handler error: {str(e)}")
        return {"error": f"Handler error: {str(e)}"}

# RunPod serverless handler
if __name__ == "__main__":
    print("🚀 Starting AI Video Generator Serverless Handler")
    print("📋 Supported models: Wan 2.2 T2V, Wan 2.2 I2V")
    runpod.serverless.start({"handler": handler})
