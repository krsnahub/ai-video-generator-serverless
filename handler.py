import runpod  # Required
from workflows import WAN_22_T2V_WORKFLOW  # etc.
import requests, time, base64, uuid

COMFYUI_URL = "http://127.0.0.1:8188"

def handler(event):
    inp = event["input"]
    # build workflow from inp like before
    return {"ok": True, "input": inp}

runpod.serverless.start({"handler": handler})  # Required
