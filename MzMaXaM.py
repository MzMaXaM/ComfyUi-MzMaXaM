import re
import comfy
import torch

class SelectLatentSize:
    def __init__(self):
        self.device = comfy.model_management.intermediate_device()
    @classmethod
    def INPUT_TYPES(s):
        return {
            'required': {
                "resolution": (
                    [
                        #Name (WidthxHeight) res
                    "Cinema landscape (1536x640) 21x9",
                    "Smartphone landscape (1472x704) 19x9",
                    "HD_Video landscape (1344x768) 16x9",
                    "Laptop landscape (1216x768) 8x5",
                    "Photo landscape (1216x832) 3x2",
                    "Widescreen landscape (1176x840) 7x5",
                    "TV landscape (1152x896) 4x3",
                    "Square (1024x1024) 1x1",
                    "TV portrait (896x1152) 4x3",
                    "Widescreen portrait (840x1176) 7x5",
                    "Photo portrait (832x1216) 3x2",
                    "Laptop portrait (768x1216) 8x5",
                    "HD_Video portrait (768x1344) 16x9",
                    "Smartphone portrait (704x1472) 19x9",
                    "Cinema portrait (640x1536) 21x9",
                ],
                {
                "default": "Square (1024x1024) 1x1"
                }),
            },
          }
    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("Latent",)
    OUTPUT_TOOLTIPS = ("Select the empty latent image resolution. And connect it to the Sampler",)
    FUNCTION = "return_size"
    OUTPUT_NODE = True
    CATEGORY = "MzMaXaM"
    DESCRIPTION = "Select size of a new empty latent image to be denoised via sampling. Name (WidthxHeight) resolution."
    def return_size(self, resolution):
        batch_size = 1
        match = re.search(r'\((\d+)x(\d+)\)', resolution)
        a, b = match.groups()
        width = int(a)
        height = int(b)
        latent = torch.zeros([batch_size, 4, height // 8, width // 8], device=self.device)
        return ({"samples":latent}, )

class TextEncode3in1:
    def __init__(self):
        self.device = comfy.model_management.intermediate_device()
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "clip": ("CLIP", {"tooltip": "The CLIP model used for encoding the text."}),
                "posTextA": ("STRING", {
                    "multiline": True, 
                    "dynamicPrompts": True, 
                    "tooltip": "The positive text to be encoded.",
                    "default": "score_9, score_8_up, score_8. score_9, score_8_up, score_7_up, score_6_up, masterpiece, 4k, high quality, "
                }), 
                "posTextB": ("STRING", {
                    "multiline": True, 
                    "dynamicPrompts": True, 
                    "tooltip": "The positive text to be encoded.",
                    "default": "1girl, solo, Sakura, pink short hair, green eyes, forehead protector, blushing, looking at viewer, smiling, white dress green background"
                }), 
                "stop_at_clip_layer": ("INT", {"default": -1, "min": -24, "max": -1, "step": 1}),
                "negText": ("STRING", {
                    "multiline": True, 
                    "dynamicPrompts": True, 
                    "tooltip": "The negative text to be encoded.",
                    "default": "score_5, score_4, worst quality, low quality, text, censored, deformed, bad hand, blurry, (watermark), weights, extra hands, extra dicks. 3 finger, bad anatomy, big head, artist signature, artist name"
                })
            }
        }
    RETURN_TYPES = ("CONDITIONING","CONDITIONING")
    RETURN_NAMES = ("Positive Conditioning", "Negative Conditioning",)
    OUTPUT_NODE = True
    OUTPUT_TOOLTIPS = ("A conditioning containing the embedded text used to guide the diffusion model.",)
    FUNCTION = "encode"
    CATEGORY = "MzMaXaM"
    DESCRIPTION = "Encodes a text prompt using a CLIP model into an embedding that can be used to guide the diffusion model towards generating specific images."
    def encode(self, clip, posTextA, posTextB, stop_at_clip_layer, negText):
        clip = clip.clone()
        clip.clip_layer(stop_at_clip_layer)
        posText = posTextA + posTextB
        tokenPos = clip.tokenize(posText)
        tokenNeg = clip.tokenize(negText)
        posOutput = clip.encode_from_tokens(tokenPos, return_pooled=True, return_dict=True)
        negOutput = clip.encode_from_tokens(tokenNeg, return_pooled=True, return_dict=True)
        posCond = posOutput.pop("cond")
        negCond = negOutput.pop("cond")
        return (
            [[posCond, posOutput]], 
            [[negCond, negOutput]], 
            )

NODE_CLASS_MAPPINGS = {
    "SelectLatentSize": SelectLatentSize,
    "TextEncode3in1":TextEncode3in1
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SelectLatentSize": "Select latent size",
    "TextEncode3in1":"Text Encoder 3 in 1"
}