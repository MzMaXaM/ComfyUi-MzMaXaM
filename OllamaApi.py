
import io
import json
import base64
import random
import requests
import numpy as np
from PIL import Image
from ollama import chat
from ollama import ChatResponse

# Fetch the list of installed models from the API
# http://localhost:11434/api/tags
# llava-phi3:latest
# bakllava:latest

def get_installed_models():
    # Fetch the list of installed models from the API
    response = requests.get("http://localhost:11434/api/tags")
    if response.status_code == 200:
        models_data = response.json()
        models = [model["name"] for model in models_data["models"]]
        print(models)
        return models
    else:
        raise ValueError("Failed to fetch installed models")

class ImageToTextOllama:
    @classmethod
    def INPUT_TYPES(cls):
        models = cls.get_installed_models()
        return {
            "required": {
                "image": ("IMAGE",),
                "prompt": ("STRING", {"default": "Describe this image in detail"}),
                "model": ("STRING", {"default": models[0], "choices": models}),
                "seed": ("INT", {"default": 1, "min": -1, "max": 0xffffffffffffffff}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Description",)
    FUNCTION = "process_image"
    CATEGORY = "MzMaXaM/WiP"
    
    @staticmethod
    def get_installed_models():
        # Fetch the list of installed models from the API
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models_data = response.json()
            models = [model["name"] for model in models_data["models"]]
            print(models)
            return models
        else:
            raise ValueError("Failed to fetch installed models")

    def process_image(self, image, prompt, model, seed):
        if seed == -1:
            seed = random.randint(0, 0xffffffffffffffff)
        random.seed(seed)
        # process image
        pil_image = Image.fromarray(np.uint8(image[0]*255))
        buffered = io.BytesIO()
        pil_image.save(buffered, format="JPEG")
        base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
        # chat with model
        try:
            response: ChatResponse = chat(model, messages=[
                {
                    'role': 'user',
                    'content': prompt + ' Json output is preferred.',
                    'images': [base64_image],
                },
            ])
            if response:
                return (response.message.content, )
            else:
                raise ValueError("API request failed")
        except Exception as e:
            raise ValueError(f"API request failed: {e}")
            
        
class TextToTextOllama:
    @classmethod
    def INPUT_TYPES(cls):
        models = get_installed_models()
        return {
            "required": {
                "prompt": ("STRING", {"default": "Generate a creative prompt for SDXL:"}),
                "model": ("STRING", {"default": models[0], "choices": models}),
                "seed": ("INT", {"default": 1, "min": -1, "max": 0xffffffffffffffff}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Generated Text",)
    FUNCTION = "generate_text"
    CATEGORY = "MzMaXaM/WiP"

    def generate_text(self, prompt, model, seed):
        if seed == -1:
            seed = random.randint(0, 0xffffffffffffffff)
        random.seed(seed)
        # chat with model
        try:
            response: ChatResponse = chat(model, messages=[
                {
                    'role': 'user',
                    'content': prompt + ' Json output is preferred.',
                },
            ])
            if response:
                return (response.message.content, )
            else:
                raise ValueError("API request failed")
        except Exception as e:
            raise ValueError(f"API request failed: {e}")

        
OLMS_CLASS_MAPPINGS = {
    "ImageToText": ImageToTextOllama,
    "TextToText": TextToTextOllama,
}

OLMS_NAME_MAPPINGS = {
    "ImageToText": "Image to Text Ollama",
    "TextToText": "Text to Text Ollama",
}