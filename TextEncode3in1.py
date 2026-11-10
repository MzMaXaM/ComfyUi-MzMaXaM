import comfy # type: ignore
import comfy.model_management # type: ignore

class TextEncode3in1:
    def __init__(self):
        pass

    @property
    def device(self):
        return comfy.model_management.intermediate_device()

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
    OUTPUT_TOOLTIPS = ("A conditioning containing the embedded text used to guide the diffusion model.",)
    FUNCTION = "encode"
    CATEGORY = "MzMaXaM"
    DESCRIPTION = ("Encodes a text prompt using a CLIP model into an embedding that can be used to guide the diffusion model towards generating specific images.\n"
                    "The text prompt is split into two parts, and the CLIP model is used to encode both parts into a single embedding.\n"
    )
    def encode(self, clip, positive_Text_A=None, positive_Text_B=None, stop_at_clip_layer=-2, negative_Text=None, **kwargs):
        if clip is None:
            raise RuntimeError("ERROR: clip input is invalid: None\n\nIf the clip is from a checkpoint loader node your checkpoint does not contain a valid clip or text encoder model.")

        if positive_Text_A is None:
            positive_Text_A = kwargs.get("posTextA", "")
        if positive_Text_B is None:
            positive_Text_B = kwargs.get("posTextB", "")
        if negative_Text is None:
            negative_Text = kwargs.get("negText", "")

        clip = clip.clone()
        if hasattr(clip, "clip_layer") and stop_at_clip_layer is not None:
            clip.clip_layer(stop_at_clip_layer)

        posTextA_str = str(positive_Text_A) if positive_Text_A is not None else ""
        posTextB_str = str(positive_Text_B) if positive_Text_B is not None else ""

        if posTextA_str and posTextB_str:
            if posTextA_str.rstrip().endswith(","):
                posText = f"{posTextA_str.rstrip()} {posTextB_str.lstrip()}"
            elif posTextA_str.endswith(("\n", " ")):
                posText = f"{posTextA_str}{posTextB_str}"
            else:
                posText = f"{posTextA_str}, {posTextB_str}"
        else:
            posText = posTextA_str or posTextB_str

        negText_str = str(negative_Text) if negative_Text is not None else ""

        tokenPos = clip.tokenize(posText)
        tokenNeg = clip.tokenize(negText_str)

        if hasattr(clip, "encode_from_tokens_scheduled"):
            posCond = clip.encode_from_tokens_scheduled(tokenPos)
            negCond = clip.encode_from_tokens_scheduled(tokenNeg)
        else:
            posOutput = clip.encode_from_tokens(tokenPos, return_pooled=True, return_dict=True)
            negOutput = clip.encode_from_tokens(tokenNeg, return_pooled=True, return_dict=True)
            pos_c = posOutput.pop("cond")
            neg_c = negOutput.pop("cond")
            posCond = [[pos_c, posOutput]]
            negCond = [[neg_c, negOutput]]

        return (posCond, negCond)

TE3_CLASS_MAPPINGS = {
    "TextEncode3in1":TextEncode3in1
}

TE3_NAME_MAPPINGS = {
    "TextEncode3in1":"Text Encoder 3 in 1"
}
