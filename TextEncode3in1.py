import comfy # type: ignore

class TextEncode3in1:
    def __init__(self):
        self.device = comfy.model_management.intermediate_device()
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "clip": ("CLIP", {"tooltip": "The CLIP model used for encoding the text."}),
                "positive_Text_A": ("STRING", {
                    "multiline": True, 
                    "dynamicPrompts": True, 
                    "tooltip": "First part of the positive text to be encoded.",
                    "default": "score_9, score_8_up, score_8. score_9, score_8_up, score_7_up, score_6_up, masterpiece, 4k, 8k, high quality, best quality, ultra high res, ultra detailed, 8k wallpaper"
                }), 
                "positive_Text_B": ("STRING", {
                    "multiline": True, 
                    "dynamicPrompts": True, 
                    "tooltip": "Second part of the positive text to be encoded.",
                    "default": "1girl, solo, Sakura, pink short hair, green eyes, forehead protector, blushing, looking at viewer, smiling, white dress green background"
                }), 
                "stop_at_clip_layer": ("INT", {
                    "default": -2, "min": -24, "max": -1, "step": 1
                    }),
                "negative_Text": ("STRING", {
                    "multiline": True, 
                    "dynamicPrompts": True, 
                    "tooltip": "The negative text to be encoded.",
                    "default": "score_5, score_4, worst quality, low quality, text, censored, deformed, bad hand, blurry, (watermark), weights, extra hands, 3 finger, bad anatomy, big head, artist signature, artist name"
                })
            }
        }
    RETURN_TYPES = ("CONDITIONING","CONDITIONING")
    RETURN_NAMES = ("Positive Conditioning", "Negative Conditioning",)
    OUTPUT_NODE = True
    OUTPUT_TOOLTIPS = ("A conditioning containing the embedded text used to guide the diffusion model.",)
    FUNCTION = "encode"
    CATEGORY = "MzMaXaM"
    DESCRIPTION = ("Encodes a text prompt using a CLIP model into an embedding that can be used to guide the diffusion model towards generating specific images.\n"
                    "The text prompt is split into two parts, and the CLIP model is used to encode both parts into a single embedding.\n"
    )
    def encode(self, clip, positive_Text_A, positive_Text_B, stop_at_clip_layer, negative_Text):
        clip = clip.clone()
        clip.clip_layer(stop_at_clip_layer)
        posText = positive_Text_A +". <BEAK>\n"+ positive_Text_B
        tokenPos = clip.tokenize(posText)
        tokenNeg = clip.tokenize(negative_Text)
        posOutput = clip.encode_from_tokens(tokenPos, return_pooled=True, return_dict=True)
        negOutput = clip.encode_from_tokens(tokenNeg, return_pooled=True, return_dict=True)
        posCond = posOutput.pop("cond")
        negCond = negOutput.pop("cond")
        return (
            [[posCond, posOutput]], 
            [[negCond, negOutput]], 
            )

TE3_CLASS_MAPPINGS = {
    "TextEncode3in1":TextEncode3in1
}

TE3_NAME_MAPPINGS = {
    "TextEncode3in1":"Text Encoder 3 in 1"
}