import comfy

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
                "stop_at_clip_layer": ("INT", {"default": -2, "min": -24, "max": -1, "step": 1}),
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

TE3_CLASS_MAPPINGS = {
    "TextEncode3in1":TextEncode3in1
}

TE3_NAME_MAPPINGS = {
    "TextEncode3in1":"Text Encoder 3 in 1"
}