import runpod
from workflows import process_data

def handler(event):
    """
    This is the handler function that will be called by RunPod.
    """
    return process_data(event["input"])

# Start the serverless worker
runpod.serverless.start({"handler": handler})
