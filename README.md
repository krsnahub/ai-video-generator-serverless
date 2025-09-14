# Wan Serverless Wrapper

RunPod serverless worker to run Wan 2.2 / 2.1 models (T2V + I2V) via ComfyUI.

## Usage
Deploy to RunPod → get endpoint → call with JSON:

```json
{
  "model_type": "wan22_t2v",
  "prompt": "A cat dancing in the street",
  "steps": 25,
  "cfg": 7.5,
  "fps": 24,
  "duration": 5
}
```
