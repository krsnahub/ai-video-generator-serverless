import runpod
import requests
import time
import os
import subprocess
import uuid
import base64
import tempfile
from PIL import Image

# Get RunPod API key
RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY")

def download_or_save_image(image_url, dest_path):
    """Download image from URL or handle data URL"""
    print(f"📥 Processing image: {image_url[:50]}...")
    
    if image_url.startswith('data:'):
        print("🔄 Processing data URL...")
        try:
            header, data = image_url.split(',', 1)
            image_data = base64.b64decode(data)
            
            with open(dest_path, 'wb') as f:
                f.write(image_data)
            
            print(f"✅ Data URL saved to: {dest_path}")
            return
        except Exception as e:
            raise Exception(f"Failed to process data URL: {str(e)}")
    else:
        print(f"📥 Downloading from URL: {image_url}")
        r = requests.get(image_url, stream=True, timeout=30)
        if r.status_code == 200:
            with open(dest_path, "wb") as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            print(f"✅ Downloaded to: {dest_path}")
        else:
            raise Exception(f"Failed to download file: {image_url} (Status: {r.status_code})")

def upload_to_runpod(local_file, filename):
    """Upload file to RunPod storage"""
    print(f"📤 Uploading: {filename}")
    try:
        res = requests.post(
            "https://api.runpod.io/storage/v2/upload",
            headers={"Authorization": f"Bearer {RUNPOD_API_KEY}"},
            json={"filename": filename},
            timeout=30
        )
        
        if res.status_code != 200:
            raise Exception(f"Failed to get upload URL: {res.status_code} - {res.text}")
        
        signed_url = res.json()["url"]

        with open(local_file, "rb") as f:
            put_res = requests.put(signed_url, data=f, timeout=60)
            if put_res.status_code not in [200, 201]:
                raise Exception(f"Upload failed: {put_res.status_code} - {put_res.text}")

        public_url = signed_url.split("?")[0]
        print(f"✅ Uploaded to: {public_url}")
        return public_url
        
    except Exception as e:
        print(f"❌ Upload failed: {str(e)}")
        raise

def generate_wan_video(input_image_path, output_video_path, prompt, duration=4):
    """Generate video using WAN (Wunjo AI) model"""
    print(f"🎬 Generating WAN video:")
    print(f"   Input: {input_image_path}")
    print(f"   Output: {output_video_path}")
    print(f"   Prompt: {prompt}")
    print(f"   Duration: {duration}s")
    
    try:
        # Method 1: Try using wunjo CLI if available
        cmd = [
            "python", "-m", "wunjo.api.video_generation",
            "--input_image", input_image_path,
            "--output_video", output_video_path,
            "--prompt", prompt,
            "--duration", str(duration),
            "--fps", "8"
        ]
        
        print(f"🎬 Running WAN: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)  # 5 min timeout
        
        if result.returncode == 0 and os.path.exists(output_video_path):
            print(f"✅ WAN video generated: {output_video_path}")
            return True
        else:
            print(f"❌ WAN CLI failed: {result.stderr}")
            
            # Method 2: Try direct Python import
            try:
                print("🔄 Trying direct WAN import...")
                
                # Try importing WAN directly
                from wunjo.video import generate_video
                
                generate_video(
                    input_image=input_image_path,
                    output_path=output_video_path,
                    prompt=prompt,
                    duration=duration,
                    fps=8
                )
                
                if os.path.exists(output_video_path):
                    print(f"✅ WAN Python API generated: {output_video_path}")
                    return True
                    
            except ImportError:
                print("❌ WAN not installed or not available")
            except Exception as e:
                print(f"❌ WAN Python API failed: {str(e)}")
            
            # Method 3: Try SVD (Stable Video Diffusion) as fallback
            try:
                print("🔄 Trying Stable Video Diffusion as fallback...")
                
                cmd_svd = [
                    "python", "-c", 
                    f"""
import torch
from diffusers import StableVideoDiffusionPipeline
from PIL import Image

# Load SVD model
pipe = StableVideoDiffusionPipeline.from_pretrained("stabilityai/stable-video-diffusion-img2vid-xt", torch_dtype=torch.float16, variant="fp16")
pipe.to("cuda" if torch.cuda.is_available() else "cpu")

# Load and process image
image = Image.open("{input_image_path}").convert("RGB")
image = image.resize((1024, 576))

# Generate video
frames = pipe(image, decode_chunk_size=8, generator=torch.manual_seed(42)).frames[0]

# Save as video
import cv2
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter("{output_video_path}", fourcc, 8.0, (1024, 576))

for frame in frames:
    frame_cv = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
    out.write(frame_cv)

out.release()
print("SVD video generated successfully")
"""
                ]
                
                result_svd = subprocess.run(cmd_svd, capture_output=True, text=True, timeout=300)
                
                if result_svd.returncode == 0 and os.path.exists(output_video_path):
                    print(f"✅ SVD fallback generated: {output_video_path}")
                    return True
                else:
                    print(f"❌ SVD fallback failed: {result_svd.stderr}")
                    
            except Exception as e:
                print(f"❌ SVD fallback error: {str(e)}")
            
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Video generation timed out")
        return False
    except Exception as e:
        print(f"❌ Video generation failed: {str(e)}")
        return False

def handler(event):
    """Main handler for WAN video generation"""
    try:
        inputs = event.get("input", {})
        image_url = inputs.get("image_url")
        prompt = inputs.get("prompt", "Generate a video from this image")
        duration = int(inputs.get("duration", 4))

        print(f"🎬 WAN Video Generation Request:")
        print(f"   Image URL type: {'data URL' if image_url and image_url.startswith('data:') else 'regular URL'}")
        print(f"   Prompt: {prompt}")
        print(f"   Duration: {duration}s")

        if not image_url:
            return {"status": "error", "message": "image_url is required"}

        # Create temp paths
        input_path = f"/tmp/input_{uuid.uuid4().hex[:8]}.png"
        output_path = f"/tmp/output_{uuid.uuid4().hex[:8]}.mp4"

        # 1. Download/save input image
        download_or_save_image(image_url, input_path)

        # 2. Generate video using WAN model
        video_created = generate_wan_video(input_path, output_path, prompt, duration)
        
        if video_created:
            # 3. Upload to RunPod storage
            video_url = upload_to_runpod(output_path, f"wan_video_{int(time.time())}.mp4")
            
            # 4. Cleanup temp files
            try:
                os.unlink(input_path)
                os.unlink(output_path)
            except:
                pass
            
            return {
                "status": "success",
                "video_url": video_url,
                "metadata": {
                    "duration": duration,
                    "fps": 8,
                    "prompt": prompt,
                    "model": "WAN"
                }
            }
        else:
            return {
                "status": "error",
                "message": "WAN video generation failed - model not available",
                "video_url": None
            }

    except Exception as e:
        print(f"❌ Handler error: {str(e)}")
        return {
            "status": "error",
            "message": f"Processing failed: {str(e)}"
        }

# Start RunPod serverless handler
runpod.serverless.start({"handler": handler})
