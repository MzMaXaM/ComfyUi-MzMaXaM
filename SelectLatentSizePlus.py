import re
import torch  # type: ignore
import comfy  # type: ignore
class selectLatentSizePlus:
    # Resolution mapping for the aspect ratios
    # I cannot connect the JSON to the aspect ratio in the UI, so I have to hardcode it here
    # This is a mapping of aspect ratios to their respective resolutions
    resolution_mapping = {
                "1:1 Square Format": [
                    "512x512",
                    "576x576",
                    "640x640",
                    "704x704",
                    "768x768",
                    "832x832",
                    "896x896",
                    "960x960",
                    "1024x1024",
                    "1088x1088",
                    "1152x1152",
                    "1216x1216",
                    "1280x1280",
                    "1344x1344",
                    "1920x1920"
                ],
                "4:5 Portrait Photography": [
                    "512x640",
                    "576x720",
                    "768x960",
                    "1024x1280",
                    "1216x1536",
                    "1280x1600",
                    "1536x1920"
                ],
                "3:4 Retro CRT TV & Monitor": [
                    "576x768",
                    "640x768",
                    "704x896",
                    "768x1024",
                    "960x1280",
                    "1088x1472",
                    "1152x1536",
                    "1440x1920"
                ],
                "2:3 Standard Photography": [
                    "512x768",
                    "576x864",
                    "640x960",
                    "704x1088",
                    "768x1152",
                    "832x1280",
                    "896x1344",
                    "960x1408",
                    "1024x1536",
                    "1152x1728",
                    "1280x1920"
                ],
                "7:10 Trading Cards of all sorts": [
                    "512x728",
                    "576x816",
                    "640x912",
                    "704x1008",
                    "768x1088",
                    "960x1344",
                    "1352x1920"
                ],
                "5:8 Expanded Portrait": [
                    "512x640",
                    "576x720",
                    "640x800",
                    "704x1152",
                    "768x1280",
                    "832x1408",
                    "960x1664",
                    "1024x1792",
                    "1088x1920"
                ],
                "7:12 Tall Vista":[
                    "512x896",
                    "576x1008",
                    "640x1120",
                    "704x1232",
                    "768x1344",
                    "832x1456",
                    "896x1536",
                    "960x1680"
                ],
                "9:16 Smartphone Screen": [
                    "512x896",
                    "576x1024",
                    "640x1152",
                    "720x1280",
                    "768x1408",
                    "832x1472",
                    "960x1728",
                    "1080x1920"
                ],
                "1:1.85 Cinematic Widescreen": [
                    "512x960",
                    "540x1024",
                    "576x1088",
                    "640x1216",
                    "704x1344",
                    "768x1472",
                    "832x1536",
                    "960x1792",
                    "1024x1920"
                ],
                "1:2 Two Fold": [
                    "512x1024",
                    "576x1152",
                    "640x1280",
                    "704x1408",
                    "768x1536",
                    "832x1664",
                    "896x1792",
                    "960x1920",
                    "1024x2048"
                ],
                "9:21 UltraWide Monitor": [
                    "512x1152",
                    "576x1280",
                    "768x1856",
                    "800x1920",
                    "896x2176"
                ],
                "1:3 Panoramic Photography": [
                    "512x1536",
                    "576x1728",
                    "640x1920",
                    "704x2048",
                    "768x2176"
                ],
                "9:32 Super UltraWide Monitor": [
                    "512x1856",
                    "540x1920",
                    "576x2048",
                    "640x2240",
                    "704x2496"
                ],
                "1:4 Panoramic Photography": [
                    "480x1920",
                    "512x2048",
                    "576x2304",
                    "640x2560",
                    "704x2816"
                ],
                "1:5 Super Panoramic Photography": [
                    "512x2560",
                    "576x2816",
                    "640x3072",
                    "704x3328",
                    "768x3584",
                    "832x3840"
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
                    # list(cls.resolution_mapping["1:1 Square Format"] + cls.resolution_mapping["3:4 Portrait Photography, Retro CRT TV & Monitor"] + cls.resolution_mapping["4:5 Instagram Portrait"] + cls.resolution_mapping["2:3 Standard Photography"]),
                    sum(list(cls.resolution_mapping.values()), []),
                    {"default": cls.resolution_mapping[cls.default_aspect_ratio][0]},
                ),
                "swap_orientation": (["enable", "disable"], {"default": "disable"}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 10}),
            }
        }
    
    RETURN_TYPES = ("LATENT", "INT", "INT")
    RETURN_NAMES = ("Latent", "Width", "Height")
    OUTPUT_TOOLTIPS = ("Empty Latent. Width and Height of selected size.",)
    FUNCTION = "generate_latent"
    OUTPUT_NODE = True
    CATEGORY = "MzMaXaM"
    DESCRIPTION = (
        "Resolution selector for different aspect ratios.\n"
        "Supports 1:1, 4:5, 3:4, 2:3, 7:10, 5:8, 7:12, 9:16, 1:1.85, 1:2, 9:21, 1:3, 9:32, 1:4 and 1:5.\n"
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
        # Validate dimensions are (essential for latent space)
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
SLSP_CLASS_MAPPINGS = {
    "selectLatentSizePlus": selectLatentSizePlus,
}
SLSP_NAME_MAPPINGS = {
    "selectLatentSizePlus": "Select Latent Size Plus",
}
# Export WEB_DIRECTORY so ComfyUI serves our JS/HTML resources.
WEB_DIRECTORY = "./js"
__all__ = ["SLSP_CLASS_MAPPINGS", "SLSP_NAME_MAPPINGS", "WEB_DIRECTORY"]