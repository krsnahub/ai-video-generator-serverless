import runpod
import requests
import base64
import uuid
import time

from workflows import (
    WAN_22_T2V_WORKFLOW,
    WAN_22_I2V_WORKFLOW,
    WAN_21_T2V_WORKFLOW,
    WAN_21_I2V_WORKFLOW,
)

COMFYUI_URL = "http://127.0.0.1:8188"


def build_workflow(inp):
    model_type = inp.get("model_type", "wan22_t2v")
    prompt = inp.get("prompt", "")
    negative = inp.get("negative_prompt", "")
    width = inp.get("width", 1280)
    height = inp.get("height", 720)
    steps = inp.get("steps", 30)
    cfg = inp.get("cfg", 7.5)
    seed = inp.get("seed", int(time.time()))
    fps = inp.get("fps", 24)
    duration = inp.get("duration", 5)
    strength = inp.get("strength", 0.8)
    image_data = inp.get("image_data")

    if model_type == "wan22_t2v":
        wf = WAN_22_T2V_WORKFLOW.copy()
        wf["1"]["inputs"]["text"] = prompt
        wf["6"]["inputs"]["text"] = negative
        wf["2"]["inputs"]["width"] = width
        wf["2"]["inputs"]["height"] = height
        wf["3"]["inputs"]["steps"] = steps
        wf["3"]["inputs"]["cfg"] = cfg
        wf["3"]["inputs"]["seed"] = seed
        wf["9"]["inputs"]["fps"] = fps
        return wf

    elif model_type == "wan22_i2v":
        if not image_data:
            raise ValueError("Image required for I2V")
        image_bytes = base64.b64decode(image_data.split(",")[1])
        image_name = f"input_{uuid.uuid4()}.png"
        files = {"image": (image_name, image_bytes, "image/png")}
        upload = requests.post(f"{COMFYUI_URL}/upload/image", files=files).json()
        wf = WAN_22_I2V_WORKFLOW.copy()
        wf["1"]["inputs"]["image"] = upload.get("name", image_name)
        wf["2"]["inputs"]["text"] = prompt
        wf["7"]["inputs"]["text"] = negative
        wf["3"]["inputs"]["steps"] = steps
        wf["3"]["inputs"]["cfg"] = cfg
        wf["3"]["inputs"]["seed"] = seed
        wf["3"]["inputs"]["denoise"] = strength
        wf["10"]["inputs"]["fps"] = fps
        return wf

    elif model_type == "wan21_t2v":
        wf = WAN_21_T2V_WORKFLOW.copy()
        wf["1"]["inputs"]["text"] = prompt
        wf["6"]["inputs"]["text"] = negative
        wf["2"]["inputs"]["width"] = width
        wf["2"]["inputs"]["height"] = height
        wf["3"]["inputs"]["steps"] = steps
        wf["3"]["inputs"]["cfg"] = cfg
        wf["3"]["inputs"]["seed"] = seed
        wf["9"]["inputs"]["fps"] = fps
        return wf

    elif model_type == "wan21_i2v":
        if not image_data:
            raise ValueError("Image required for I2V")
        image_bytes = base64.b64decode(image_data.split(",")[1])
        image_name = f"input_{uuid.uuid4()}.png"
        files = {"image": (image_name, image_bytes, "image/png")}
        upload = requests.post(f"{COMFYUI_URL}/upload/image", files=files).json()
        wf = WAN_21_I2V_WORKFLOW.copy()
        wf["1"]["inputs"]["image"] = upload.get("name", image_name)
        wf["2"]["inputs"]["text"] = prompt
        wf["7"]["inputs"]["text"] = negative
        wf["3"]["inputs"]["steps"] = steps
        wf["3"]["inputs"]["cfg"] = cfg
        wf["3"]["inputs"]["seed"] = seed
        wf["3"]["inputs"]["denoise"] = strength
        wf["10"]["inputs"]["fps"] = fps
        return wf

    else:
        raise ValueError(f"Unknown model_type {model_type}")


def handler(job):
    try:
        inp = job["input"]
        workflow = build_workflow(inp)

        res = requests.post(
            f"{COMFYUI_URL}/prompt", json={"prompt": workflow}
        ).json()

        return {
            "success": True,
            "model_type": inp.get("model_type"),
            "prompt_id": res.get("prompt_id"),
            "workflow_used": workflow
        }
    except Exception as e:
        return {"error": str(e)}


runpod.serverless.start({"handler": handler})
