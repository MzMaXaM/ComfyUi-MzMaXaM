import os
import folder_paths
import uuid
from PIL import Image
import numpy as np

class ChooserImageDialog:
    def __init__(self):
        self.node = None
        self.select_index = None

    def show(self, images, node):
        self.select_index = None
        self.node = node

class ImageChooser:
    CATEGORY = "MzMaXaM/WiP/ImageSelector"
    DESCRIPTION = "Choose images to process and connect them to the next node."
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("Image",)
    OUTPUT_TOOLTIPS = ("Select the images to process",)
    FUNCTION = "choose_images"
    OUTPUT_NODE = True

    def __init__(self):
        self.selected = set()
        self.anti_selected = set()
        self.select_index = None

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"images": ("IMAGE",)},}

    def choose_images(self, images):
        dialog = ChooserImageDialog()
        dialog.show(images, self)

        # Pause the queue to wait for user input
        input("Press Enter after selecting images...")

        # Return the selected image
        if self.select_index is not None and 0 <= self.select_index < len(images):
            selected_image = images[self.select_index]
            return (selected_image,)
        else:
            print("Error: Invalid selection. Returning the first image as default.")
            return (images[0],)  # Return the first image as default

    def ui(self):
        # Generate previews and return file paths
        preview_paths = []
        images = self.input_args["images"]
        if len(images.shape) == 3:
            images = images.unsqueeze(0)
        for i in range(images.shape[0]):
            # Generate a unique filename
            filename = str(uuid.uuid4()) + ".png"
            filepath = os.path.join(folder_paths.get_temp_directory(), filename)
            # Save the image
            img = images[i].permute(1, 2, 0).cpu().numpy()
            img = (img * 255).astype(np.uint8)
            Image.fromarray(img).save(filepath)
            preview_paths.append(filepath)
            print(f"Generated preview image: {filepath}")  # Debugging statement

        return {"images": "IMAGE", "preview_paths": preview_paths}

IC_CLASS_MAPPINGS = {
    "ImageChooser": ImageChooser,
}

IC_NAME_MAPPINGS = {
    "ImageChooser": "Select a Image",
}
