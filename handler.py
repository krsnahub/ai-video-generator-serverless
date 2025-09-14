import runpod  # Required

def handler(event):
    input_data = event["input"]
    return {"echo": input_data}

runpod.serverless.start({"handler": handler})  # Required
