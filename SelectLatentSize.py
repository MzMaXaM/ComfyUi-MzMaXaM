import re
import math
import torch
import comfy
from typing import Tuple, Dict

class SelectLatentSize1Mp:
    def __init__(self):
        self.device = comfy.model_management.intermediate_device()
    @classmethod
    def INPUT_TYPES(s):
        return {
            'required': {
                "resolution": (
                    [
                    "Cinema landscape (1536x640) 21x9",#2.4
                    "Smartphone landscape (1472x704) 19x9",#2.09
                    "Hd Wide landscape (1344x712) 17x9",#1.88
                    "HD Video landscape (1280x720) 16x9",#1.77
                    "Laptop landscape (1216x768) 8x5",#1.58
                    "Photo landscape (1216x840) 3x2",#1.46
                    "Widescreen landscape (1176x840) 7x5",#1.4
                    "TV landscape (1152x896) 4x3",#1.28
                    "Square (1024x1024) 1x1",#1
                    "TV portrait (896x1152) 4x3",#0.78
                    "Widescreen portrait (840x1176) 7x5",#0.71
                    "Photo portrait (832x1216) 3x2",#0.68
                    "Laptop portrait (768x1216) 8x5",#0.63
                    "HD Video portrait (720x1280) 16x9",#0.56
                    "Hd Wide portrait (712x1344) 17x9",#0.53
                    "Smartphone portrait (704x1472) 19x9",#0.48
                    "Cinema portrait (640x1536) 21x9",#0.42
                ],
                {
                "default": "Square (1024x1024) 1x1"
                }),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 10}),
            },
          }
    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("Latent",)
    OUTPUT_TOOLTIPS = ("Select the empty latent image resolution. And connect it to the Sampler",)
    FUNCTION = "return_size"
    OUTPUT_NODE = True
    CATEGORY = "MzMaXaM"
    DESCRIPTION = "Select size of a new empty latent image to be denoised via sampling. Name (WidthxHeight) resolution."
    def return_size(self, resolution, batch_size):
        match = re.search(r'\((\d+)x(\d+)\)', resolution)
        a, b = match.groups()
        width = int(a)
        height = int(b)
        latent = torch.zeros([batch_size, 4, height // 8, width // 8], device=self.device)
        return ({"samples":latent}, )

class SelectLatentSize2Mp:
    def __init__(self):
        self.device = comfy.model_management.intermediate_device()
    @classmethod
    def INPUT_TYPES(s):
        return {
            'required': {
                "resolution": (
                    [
                    "Cinema landscape (2176x960) 21x9",#2.26
                    "Smartphone landscape (2080x992) 19x9",#2.09
                    "HD Wide landscape (1904x1008) 17x9",#1.89
                    "HD Video landscape (1920x1080) 16x9",#1.77
                    "Laptop landscape (1720x1088) 8x5",#1.58
                    "Photo landscape (1720x1184) 3x2",#1.45
                    "Widescreen landscape (1664x1184) 7x5",#1.4
                    "TV landscape (1632x1280) 4x3",#1.28
                    "Square (1448x1448) 1x1",#1
                    "TV portrait (1280x1632) 4x3",#0.78
                    "Widescreen portrait (1184x1664) 7x5",#0.71
                    "Photo portrait (1184x1720) 3x2",#0.68
                    "Laptop portrait (1088x1720) 8x5",#0.63
                    "HD Video portrait (1080x1920) 16x9",#0.56
                    "HD Wide portrait (1008x1904) 17x9",#0.53
                    "Smartphone portrait (992x2080) 19x9",#0.48
                    "Cinema portrait (960x2176) 21x9",#0.44
                ],
                {
                "default": "Square (1448x1448) 1x1"
                }),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 10}),
            },
          }
    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("Latent",)
    OUTPUT_TOOLTIPS = ("Select the empty latent image resolution. And connect it to the Sampler",)
    FUNCTION = "return_size"
    OUTPUT_NODE = True
    CATEGORY = "MzMaXaM/WiP"
    DESCRIPTION = "Select size of a new empty latent image to be denoised via sampling. Name (WidthxHeight) resolution."
    def return_size(self, resolution, batch_size):
        match = re.search(r'\((\d+)x(\d+)\)', resolution)
        a, b = match.groups()
        width = int(a)
        height = int(b)
        latent = torch.zeros([batch_size, 4, height // 8, width // 8], device=self.device)
        return ({"samples":latent}, )

SLS_CLASS_MAPPINGS = {
    "SelectLatentSize1MP": SelectLatentSize1Mp,
    "SelectLatentSize2MP": SelectLatentSize2Mp,
}

SLS_NAME_MAPPINGS = {
    "SelectLatentSize1MP": "Select latent size 1Mp",
    "SelectLatentSize2MP": "Select latent size 2Mp",
}