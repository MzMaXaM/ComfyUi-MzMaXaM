import re
import torch  # type: ignore
import comfy  # type: ignore
class newLatentAdvanced:
    # Resolution mapping for the two aspect ratios
    resolution_mapping = {
        "1:1 Square Format": [
            "Divisible by 64 512x512",
            "Divisible by 64 576x576",
            "Divisible by 64 640x640",
            "Divisible by 64 704x704",
            "Divisible by 64 768x768",
            "Divisible by 64 832x832",
            "Divisible by 64 896x896",
            "Divisible by 64 960x960",
            "Divisible by 64 1024x1024",
            "Divisible by 64 1088x1088",
            "Divisible by 64 1152x1152",
            "Divisible by 64 1216x1216",
            "Divisible by 64 1280x1280",
            "Divisible by 64 1344x1344",
            "Divisible by 64 1920x1920"
        ],
        "3:4 Portrait Photography, Retro CRT TV & Monitor": [
            "Divisible by 64 576x768",
            "Divisible by 64 768x576",
            "Divisible by 64 768x1024",
            "Divisible by 64 960x1280",
            "Divisible by 64 1024x768",
            "Divisible by 8 1088x1472",
            "Divisible by 8 1472x1088",
            "Divisible by 64 1152x1536",
            "Divisible by 64 1280x960",
            "Divisible by 64 1440x1920",
            "Divisible by 64 1536x1152",
            "Divisible by 64 1920x1440"
        ],
        "4:5 Instagram Portrait": [
            "Divisible by 64 768x960",
            "Divisible by 64 960x768",
            "Divisible by 64 1024x1280",
            "Divisible by 64 1216x1536",
            "Divisible by 64 1280x1024",
            "Divisible by 64 1280x1600",
            "Divisible by 64 1536x1216",
            "Divisible by 64 1536x1920",
            "Divisible by 64 1600x1280",
            "Divisible by 64 1920x1536"
        ],
        "2:3 Standard Photography": [
            "Divisible by 64 512x768",
            "Divisible by 64 768x512",
            "Divisible by 64 768x1152",
            "Divisible by 64 896x1344",
            "Divisible by 64 1024x1536",
            "Divisible by 64 1152x768",
            "Divisible by 64 1152x1728",
            "Divisible by 64 1280x1920",
            "Divisible by 64 1344x896",
            "Divisible by 64 1536x1024",
            "Divisible by 64 1728x1152",
            "Divisible by 64 1920x1280"
        ]
    }
    default_aspect_ratio = "1:1 Square Format"
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
                    list(cls.resolution_mapping["1:1 Square Format"] + cls.resolution_mapping["3:4 Portrait Photography, Retro CRT TV & Monitor"] + cls.resolution_mapping["4:5 Instagram Portrait"] + cls.resolution_mapping["2:3 Standard Photography"]),
                    {"default": cls.resolution_mapping[cls.default_aspect_ratio][0]},
                ),
                "swap_orientation": (["enable", "disable"], {"default": "disable"}),
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
    def generate_latent(self, aspect_ratio, resolution, batch_size, swap_orientation):
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

        # Swap dimensions if requested
        if swap_orientation == "enable":
            latent = latent.permute(0, 1, 3, 2)
            width, height = height, width

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