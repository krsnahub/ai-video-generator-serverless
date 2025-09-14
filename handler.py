# Minimal Version (less readable)
import runpod
from workflows import process_data

def handler(event):
    return process_data(event["input"])

runpod.serverless.start({"handler": handler})
