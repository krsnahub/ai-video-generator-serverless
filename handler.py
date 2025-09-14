import runpod  # Required

def handler(event):
    # Example input
    input_data = event["input"]

    # Just echo back for now
    return {"echo": input_data}

runpod.serverless.start({"handler": handler})  # Required
