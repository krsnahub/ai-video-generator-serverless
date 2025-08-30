import runpod
import requests
import os
import subprocess

def handler(event):
    inputs = event["input"]
    image_url = inputs.get("image_url")
    prompt = inputs.get("prompt", "")
    fps = inputs.get("fps", 8)
    num_frames = inputs.get("num_frames", 40)

    # TODO: replace this stub with actual call to Wan
    fake_output_url = f"https://example.com/fake_video_{fps}fps_{num_frames}f.mp4"

    return {
        "status": "success",
        "video_url": fake_output_url,
        "debug": {
            "image_url": image_url,
            "prompt": prompt,
            "fps": fps,
            "num_frames": num_frames
        }
    }

runpod.serverless.start({"handler": handler})
