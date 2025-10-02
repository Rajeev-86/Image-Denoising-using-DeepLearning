import requests
import base64
import json

SPACE_URL = "https://Rexy-3d-Denoiser-Server.hf.space"
MODEL_NAME = "model_unet" # possible values: model_unet, model_runet, model_arunet
INPUT_FILE_PATH = "input.png"
OUTPUT_FILE_PATH = "output.png"

url = f"{SPACE_URL}/predictions/{MODEL_NAME}"
print(f"Sending request to {url} with file {INPUT_FILE_PATH}...")
with open(INPUT_FILE_PATH, "rb") as f:
    response = requests.post(url, data=f)

# Check for success
response.raise_for_status()

# Try to save the output as a file (assume binary image, like curl)
try:
    with open(OUTPUT_FILE_PATH, "wb") as out:
        out.write(response.content)
    print(f"\n Success! Denoised image saved to {OUTPUT_FILE_PATH}")
except Exception as e:
    print(f"\n Error saving output: {e}")
    print(f"Raw response content: {response.content[:500]}...")