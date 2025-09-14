#!/usr/bin/env python3
"""
AI Video Generator - RunPod Endpoint Tester
Test your serverless deployment with various scenarios
"""

import requests
import json
import time
import base64
import os
from datetime import datetime

# Configuration
RUNPOD_ENDPOINT_ID = "YOUR_ENDPOINT_ID_HERE"  # Replace with your endpoint ID
RUNPOD_API_KEY = "YOUR_API_KEY_HERE"  # Replace with your API key

# API Configuration
BASE_URL = f"https://api.runpod.ai/v2/{RUNPOD_ENDPOINT_ID}"
HEADERS = {
    "Authorization": f"Bearer {RUNPOD_API_KEY}",
    "Content-Type": "application/json"
}

def test_text_to_video():
    """Test Wan 2.2 Text-to-Video generation"""
    print("🎬 Testing Wan 2.2 Text-to-Video...")
    
    payload = {
        "input": {
            "model_type": "wan22_t2v",
            "prompt": "A serene mountain lake at sunset with gentle ripples on the water, cinematic lighting, peaceful atmosphere",
            "negative_prompt": "blurry, low quality, distorted, watermark",
            "width": 1280,
            "height": 720,
            "steps": 20,  # Faster for testing
            "cfg": 7.5,
            "seed": 42  # Fixed seed for reproducible results
        }
    }
    
    try:
        # Submit job
        print("📋 Submitting T2V job...")
        response = requests.post(f"{BASE_URL}/run", json=payload, headers=HEADERS)
        response.raise_for_status()
        
        job_data = response.json()
        job_id = job_data.get("id")
        
        if not job_id:
            print(f"❌ No job ID returned: {job_data}")
            return False
        
        print(f"✅ Job submitted: {job_id}")
        
        # Wait for completion
        return wait_for_completion(job_id, "t2v_test_video.mp4")
        
    except Exception as