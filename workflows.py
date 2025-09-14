# workflows.py

import copy
from runpod_comfyui import ComfyUI

"""
Wan Video Generator - Workflows
Contains ComfyUI JSON workflows for all supported Wan models
(2.2 T2V, 2.2 I2V, 2.1 T2V, 2.1 I2V)
"""

# Wan 2.2 Text-to-Video
WAN_22_T2V_WORKFLOW = {
    "1": {"inputs": {"text": "prompt goes here", "clip": ["4", 1]}, "class_type": "CLIPTextEncode"},
    "2": {"inputs": {"width": 1280, "height": 720, "batch_size": 1}, "class_type": "EmptyLatentImage"},
    "3": {"inputs": {"seed": 42, "steps": 30, "cfg": 7.5, "sampler_name": "euler", "scheduler": "normal", "denoise": 1.0, "model": ["5", 0], "positive": ["1", 0], "negative": ["6", 0], "latent_image": ["2", 0]}, "class_type": "KSampler"},
    "4": {"inputs": {"clip_name": "wan2.2_text_encoder.safetensors"}, "class_type": "CLIPLoader"},
    "5": {"inputs": {"unet_name": "wan2.2_t2v_unet.safetensors"}, "class_type": "UNETLoader"},
    "6": {"inputs": {"text": "", "clip": ["4", 1]}, "class_type": "CLIPTextEncode"},
    "7": {"inputs": {"vae_name": "wan2.2_vae.safetensors"}, "class_type": "VAELoader"},
    "8": {"inputs": {"samples": ["3", 0], "vae": ["7", 0]}, "class_type": "VAEDecode"},
    "9": {"inputs": {"filename_prefix": "wan22_video_", "fps": 24, "images": ["8", 0]}, "class_type": "VHS_VideoCombine"}
}

# Wan 2.2 Image-to-Video
WAN_22_I2V_WORKFLOW = {
    "1": {"inputs": {"image": "input.png", "upload": "image"}, "class_type": "LoadImage"},
    "2": {"inputs": {"text": "prompt goes here", "clip": ["5", 1]}, "class_type": "CLIPTextEncode"},
    "3": {"inputs": {"seed": 42, "steps": 30, "cfg": 7.5, "sampler_name": "euler", "scheduler": "normal", "denoise": 0.8, "model": ["6", 0], "positive": ["2", 0], "negative": ["7", 0], "latent_image": ["4", 0]}, "class_type": "KSampler"},
    "4": {"inputs": {"pixels": ["1", 0], "vae": ["8", 0]}, "class_type": "VAEEncode"},
    "5": {"inputs": {"clip_name": "wan2.2_text_encoder.safetensors"}, "class_type": "CLIPLoader"},
    "6": {"inputs": {"unet_name": "wan2.2_i2v_unet.safetensors"}, "class_type": "UNETLoader"},
    "7": {"inputs": {"text": "", "clip": ["5", 1]}, "class_type": "CLIPTextEncode"},
    "8": {"inputs": {"vae_name": "wan2.2_vae.safetensors"}, "class_type": "VAELoader"},
    "9": {"inputs": {"samples": ["3", 0], "vae": ["8", 0]}, "class_type": "VAEDecode"},
    "10": {"inputs": {"filename_prefix": "wan22_i2v_", "fps": 24, "images": ["9", 0]}, "class_type": "VHS_VideoCombine"}
}

# Wan 2.1 Text-to-Video
WAN_21_T2V_WORKFLOW = {
    "1": {"inputs": {"text": "prompt goes here", "clip": ["4", 1]}, "class_type": "CLIPTextEncode"},
    "2": {"inputs": {"width": 832, "height": 480, "batch_size": 1}, "class_type": "EmptyLatentImage"},
    "3": {"inputs": {"seed": 42, "steps": 25, "cfg": 7.0, "sampler_name": "euler", "scheduler": "normal", "denoise": 1.0, "model": ["5", 0], "positive": ["1", 0], "negative": ["6", 0], "latent_image": ["2", 0]}, "class_type": "KSampler"},
    "4": {"inputs": {"clip_name": "wan2.1_text_encoder.safetensors"}, "class_type": "CLIPLoader"},
    "5": {"inputs": {"unet_name": "wan2.1_t2v_unet.safetensors"}, "class_type": "UNETLoader"},
    "6": {"inputs": {"text": "", "clip": ["4", 1]}, "class_type": "CLIPTextEncode"},
    "7": {"inputs": {"vae_name": "wan2.1_vae.safetensors"}, "class_type": "VAELoader"},
    "8": {"inputs": {"samples": ["3", 0], "vae": ["7", 0]}, "class_type": "VAEDecode"},
    "9": {"inputs": {"filename_prefix": "wan21_video_", "fps": 24, "images": ["8", 0]}, "class_type": "VHS_VideoCombine"}
}

# Wan 2.1 Image-to-Video
WAN_21_I2V_WORKFLOW = {
    "1": {"inputs": {"image": "input.png", "upload": "image"}, "class_type": "LoadImage"},
    "2": {"inputs": {"text": "prompt goes here", "clip": ["5", 1]}, "class_type": "CLIPTextEncode"},
    "3": {"inputs": {"seed": 42, "steps": 25, "cfg": 7.0, "sampler_name": "euler", "scheduler": "normal", "denoise": 0.8, "model": ["6", 0], "positive": ["2", 0], "negative": ["7", 0], "latent_image": ["4", 0]}, "class_type": "KSampler"},
    "4": {"inputs": {"pixels": ["1", 0], "vae": ["8", 0]}, "class_type": "VAEEncode"},
    "5": {"inputs": {"clip_name": "wan2.1_text_encoder.safetensors"}, "class_type": "CLIPLoader"},
    "6": {"inputs": {"unet_name": "wan2.1_i2v_unet.safetensors"}, "class_type": "UNETLoader"},
    "7": {"inputs": {"text": "", "clip": ["5", 1]}, "class_type": "CLIPTextEncode"},
    "8": {"inputs": {"vae_name": "wan2.1_vae.safetensors"}, "class_type": "VAELoader"},
    "9": {"inputs": {"samples": ["3", 0], "vae": ["8", 0]}, "class_type": "VAEDecode"},
    "10": {"inputs": {"filename_prefix": "wan21_i2v_", "fps": 24, "images": ["9", 0]}, "class_type": "VHS_VideoCombine"}
}

# Map for easy access
WORKFLOWS = {
    "wan22_t2v": WAN_22_T2V_WORKFLOW,
    "wan22_i2v": WAN_22_I2V_WORKFLOW,
    "wan21_t2v": WAN_21_T2V_WORKFLOW,
    "wan21_i2v": WAN_21_I2V_WORKFLOW,
}

# This function processes the input and runs the ComfyUI job
def process_data(job_input):
    """
    Takes the job input, selects and configures the correct ComfyUI workflow,
    and runs the job.
    """
    workflow_id = job_input.get("workflow", "wan22_t2v")
    if workflow_id not in WORKFLOWS:
        return {"error": f"Workflow '{workflow_id}' not found."}

    workflow = copy.deepcopy(WORKFLOWS[workflow_id])

    prompt = job_input.get("prompt", "a beautiful video")
    negative_prompt = job_input.get("negative_prompt", "")
    seed = job_input.get("seed")

    # Find prompt nodes and update them
    for node_id, node in workflow.items():
        if node["class_type"] == "CLIPTextEncode":
            # In KSampler, "positive" points to the positive prompt node ID.
            # We check which node is linked to the KSampler's "positive" input.
            is_positive = any(
                n.get("inputs", {}).get("positive", [None])[0] == node_id
                for n in workflow.values() if n.get("class_type") == "KSampler"
            )
            if is_positive:
                node["inputs"]["text"] = prompt
            else:
                node["inputs"]["text"] = negative_prompt

    # Find KSampler node and update seed
    for node in workflow.values():
        if node["class_type"] == "KSampler" and seed is not None:
            node["inputs"]["seed"] = seed

    # Handle image input for I2V models
    if "i2v" in workflow_id:
        input_image = job_input.get("input_image")
        if not input_image:
            return {"error": "Image-to-video models require an 'input_image'."}
        for node in workflow.values():
            if node["class_type"] == "LoadImage":
                node["inputs"]["image"] = input_image

    # Run the ComfyUI job
    comfyui = ComfyUI()
    comfyui.queue_prompt(workflow)
    output = comfyui.get_output()

    return output
