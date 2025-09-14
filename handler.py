import runpod
from workflows import process_data  # <-- THIS IS THE CRUCIAL LINE TO ADD

def handler(event):
    """
    This is the handler function that will be called by RunPod.
    """
    input_data = event["input"]
    
    # Process the input using the function from workflows.py
    result = process_data(input_data)
    
    # Return the result
    return result

# Start the serverless worker
runpod.serverless.start({"handler": handler})
