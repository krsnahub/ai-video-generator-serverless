import runpod
import requests
import time
import os

# Get API key and endpoint from environment variables (set in RunPod console)
RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY")
ENDPOINT_ID = os.getenv("RUNPOD_ENDPOINT_ID")

def handler(event):
    inputs = event.get("input", {})
    image_url = inputs.get("image_url")
    prompt = inputs.get("prompt", "")
    fps = inputs.get("fps", 8)
    num_frames = inputs.get("num_frames", 40)

    # Submit job to RunPod
    submit_url = f"https://api.runpod.io/v2/{ENDPOINT_ID}/run"
    headers = {"Authorization": f"Bearer {RUNPOD_API_KEY}"}
    payload = {
        "input": {
            "image_url": image_url,
            "prompt": prompt,
            "fps": fps,
            "num_frames": num_frames
        }
    }

    submit_res = requests.post(submit_url, json=payload, headers=headers)
    job = submit_res.json()
    job_id = job.get("id")

    if not job_id:
        return {"status": "error", "message": f"Failed to submit job: {job}"}

    # Poll until job is done
    status_url = f"https://api.runpod.io/v2/{ENDPOINT_ID}/status/{job_id}"
    while True:
        res = requests.get(status_url, headers=headers).json()
        status = res.get("status")

        if status == "COMPLETED":
            output = res.get("output", {})
            video_url = output.get("video_url") or output.get("url")
            return {
                "status": "success",
                "video_url": video_url,
                "debug": output
            }
        elif status == "FAILED":
            return {"status": "failed", "debug": res}

        time.sleep(2)  # wait before polling again


# Start RunPod serverless handler
runpod.serverless.start({"handler": handler})
