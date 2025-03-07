import torch
import numpy as np
from PIL import Image
import io
import base64
import os

class ImageDisplay:
    def __init__(self):
        self.html_path = os.path.join(os.path.dirname(__file__), "Play1.html")  # Path to HTML

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
            }
        }

    CATEGORY = "Play1"
    DESCRIPTION = "Display images in the browser."
    RETURN_TYPES = ()
    FUNCTION = "display_images"

    def display_images(self, images):
        base64_images = []
        for image in images:
            img_array = image.cpu().numpy()
            # More robust normalization:
            img_array = (img_array - img_array.min()) / (img_array.max() - img_array.min())  # Normalize 0-1
            i = 255. * img_array
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            base64_images.append(img_str)

        return {"base64_images": base64_images}  # Return ONLY the image data

    def to_html(self, data):  # The crucial missing method!
        with open(self.html_path, 'r', encoding='utf-8') as f:
            html = f.read()
        return {"html": html}

ID_NODE_CLASS_MAPPINGS = {
    "ImageDisplay": ImageDisplay,
}

ID_NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageDisplay": "Select an Image",
}
