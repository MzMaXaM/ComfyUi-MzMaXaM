import re
import torch  # type: ignore
import comfy  # type: ignore
class newLatentAdvanced:
    # Resolution mapping for the two aspect ratios
    resolution_mapping = {
        "Square Format Photography (1:1)": [
            "1920x1920",
            "3840x3840",
            "7680x7680",
            "1344x1344",
            "1280x1280",
            "1216x1216",
            "1152x1152",
            "1088x1088",
            "1024x1024",
            "960x960",
            "896x896",
            "832x832",
            "768x768",
            "704x704",
            "640x640",
            "576x576",
            "512x512",
        ],
        "Horizontal Portrait Photography (4:5)": [
            "1920x1536",
            "3840x3072",
            "7680x6144",
            "1600x1280",
            "1536x1216",
            "1280x1024",
            "960x768",
        ]
    }
    default_aspect_ratio = "Square Format Photography (1:1)"
    def __init__(self):
        self.device = comfy.model_management.intermediate_device()
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "aspect_ratio": (
                    list(cls.resolution_mapping.keys()),
                    {"default": cls.default_aspect_ratio},
                ),
                "resolution": (
                    list(cls.resolution_mapping[cls.default_aspect_ratio]),
                    {"default": "1024x1024"},
                ),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 10}),
            }
        }
    
    RETURN_TYPES = ("LATENT", "INT", "INT")
    RETURN_NAMES = ("Latent", "Width", "Height")
    OUTPUT_TOOLTIPS = ("Select the resolution and format for a new latent image. Toggle orientation.",)
    FUNCTION = "generate_latent"
    OUTPUT_NODE = True
    CATEGORY = "MzMaXaM/WiP"
    DESCRIPTION = (
        "Advanced resolution selector for Square Format and Horizontal Portrait photography aspect ratios. "
        "Provides curated resolution options for easy selection."
    )
    def generate_latent(self, aspect_ratio, resolution, batch_size):
        # Parse resolution string ("WIDTHxHEIGHT")
        match = re.search(r"(\d+)x(\d+)", str(resolution)) # Ensure resolution is treated as string
        if not match:
            # Handle cases where the string format is unexpected (e.g., not "WxH")
            print(f"Warning: Invalid resolution string format received: '{resolution}'. Expected format 'WIDTHxHEIGHT'. Using default 1024x1024.")
            width, height = 1024, 1024 # Default to a safe value if parsing fails
        else:
            try:
                # Convert captured groups to integers
                width, height = map(int, match.groups())
            except ValueError:
                # Handle cases where parts are not valid integers (e.g., "1024x1024")
                print(f"Warning: Could not convert resolution parts to integers: '{resolution}'. Using default 1024x1024.")
                width, height = 1024, 1024 # Default to a safe value if conversion fails
        # **********************************************************************
        if batch_size <= 0:
            # This check remains important
            raise ValueError("Batch size must be a positive integer.")
        # Validate dimensions are divisible by 8 (essential for latent space)
        if width % 8 != 0 or height % 8 != 0:
            print(f"Warning: Resolution {width}x{height} is not divisible by 8. Rounding down to nearest multiple of 8.")
            width = (width // 8) * 8
            height = (height // 8) * 8
            if width == 0: width = 8 # Prevent zero dimension after rounding
            if height == 0: height = 8 # Prevent zero dimension after rounding
        latent = torch.zeros([batch_size, 4, height // 8, width // 8], device=self.device)
        # Return the latent, and the *actual* width/height used after potential rounding
        return ({"samples": latent}, width, height)
# Register the node with ComfyUI.
NLA_CLASS_MAPPINGS = {
    "newLatentAdvanced": newLatentAdvanced,
}
NLA_NAME_MAPPINGS = {
    "newLatentAdvanced": "Select new latent image Advanced",
}
# Export WEB_DIRECTORY so ComfyUI serves our JS/HTML resources.
WEB_DIRECTORY = "./js"
__all__ = ["NLA_CLASS_MAPPINGS", "NLA_NAME_MAPPINGS", "WEB_DIRECTORY"]