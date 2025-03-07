
import base64
import requests
import json
import numpy as np
from PIL import Image
import io
import random

class ImageToText:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "user_prompt": ("STRING", {"default": "Describe this image in detail"}),
                "model": ("STRING", {"default": "llava-1.6-mistral-7b"}),
                "ip_address": ("STRING", {"default": "localhost"}),
                "port": ("INT", {"default": 1234, "min": 1, "max": 65535}),
                "seed": ("INT", {"default": 1, "min": -1, "max": 0xffffffffffffffff}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Description",)
    FUNCTION = "process_image"
    CATEGORY = "MzMaXaM/WiP/LMS"

    def process_image(self, image, user_prompt, model, ip_address, port, seed):
        if seed == -1:
            seed = random.randint(0, 0xffffffffffffffff)
        random.seed(seed)
        try:
            pil_image = Image.fromarray(np.uint8(image[0]*255))
            buffered = io.BytesIO()
            pil_image.save(buffered, format="JPEG")
            base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
            payload = {
                "model": model,
                "prompt": user_prompt,
                "temperature": 0.7,
                "max_tokens": 100,
                "seed": seed
            }
            url = f"http://{ip_address}:{port}/v1/completions"
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                generatedText = data.get("choices", [{}])[0].get("text", "No response")
            else:
                print(f"Error: {response.status_code} - {response.text}")
            return (generatedText,)
        except requests.exceptions.RequestException as e:
            error_message = f"Error communicating with the server: {str(e)}"
            print(error_message)
            return (error_message,)
        except Exception as e:
            error_message = f"Unexpected error: {str(e)}"
            print(error_message)
            return (error_message,)
        
class TextToText:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "Generate a creative prompt for SDXL:"}),
                "model": ("STRING", {"default": "llava-1.6-mistral-7b"}),
                "ip_address": ("STRING", {"default": "localhost"}),
                "port": ("INT", {"default": 1234, "min": 1, "max": 65535}),
                "seed": ("INT", {"default": 1, "min": -1, "max": 0xffffffffffffffff}),
            },
            "optional": {
                "max_tokens": ("INT", {"default": 100, "min": 1, "max": 4096}),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 2.0}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Generated Text",)
    FUNCTION = "generate_text"
    CATEGORY = "MzMaXaM/WiP/LMS"

    def generate_text(self, prompt, model, ip_address, port, seed, max_tokens=100, temperature=0.7):
        if seed == -1:
            seed = random.randint(0, 0xffffffffffffffff)
        random.seed(seed)

        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature,
            }
            url = f"http://{ip_address}:{port}/v1/completions"
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                generatedText = data.get("choices", [{}])[0].get("text", "No response")
            else:
                print(f"Error: {response.status_code} - {response.text}")
            return (generatedText,)

        except requests.exceptions.RequestException as e:
            error_message = f"Error communicating with the server: {str(e)}"
            print(error_message)
            return (error_message,)
        except Exception as e:
            error_message = f"Unexpected error: {str(e)}"
            print(error_message)
            return (error_message,)
        
LMS_CLASS_MAPPINGS = {
    "LmsImageToText": ImageToText,
    "LmsTextToText": TextToText,
}

LMS_NAME_MAPPINGS = {
    "LmsImageToText": "Image to Text LMStudio",
    "LmsTextToText": "Text to Text LMStudio",
}