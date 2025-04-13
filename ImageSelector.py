class ImageChooser:
    CATEGORY = "MzMaXaM/WiP/ImageSelector"
    DESCRIPTION = "Choose one image from a batch to process."
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("Image",)
    OUTPUT_TOOLTIPS = ("Selected image from batch",)
    FUNCTION = "choose_images"
    OUTPUT_NODE = True
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "selected_index": ("INT", {
                    "default": 0, 
                    "min": 0, 
                    "max": 0,  # Will be updated dynamically
                    "step": 1,
                    "display": "slider"
                }),
            },
        }

    def choose_images(self, images, selected_index):
        # Handle single image case
        if len(images.shape) == 3:
            images = images.unsqueeze(0)
            
        max_index = images.shape[0] - 1
        if max_index < 0:
            raise ValueError("Image batch cannot be empty")
            
        # Update max value for slider
        self.__class__.INPUT_TYPES()["required"]["selected_index"][1]["max"] = max_index
        
        # Ensure selected_index is within bounds
        selected_index = max(0, min(selected_index, max_index))
        return (images[selected_index],)

IC_CLASS_MAPPINGS = {
    "ImageChooser": ImageChooser,
}

IC_NAME_MAPPINGS = {
    "ImageChooser": "Select an Image",
}