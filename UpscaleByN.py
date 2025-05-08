import math
import comfy # type: ignore
from typing import Tuple, Dict

def repeat(samples, amount):
        if isinstance(samples, tuple):
            samples = samples[0]
        s = samples.copy()
        s_in = samples["samples"]

        s["samples"] = s_in.repeat((amount, 1, 1, 1))
        if "noise_mask" in samples and samples["noise_mask"].shape[0] > 1:
            masks = samples["noise_mask"]
            if masks.shape[0] < s_in.shape[0]:
                masks = masks.repeat(math.ceil(s_in.shape[0] / masks.shape[0]), 1, 1, 1)[:s_in.shape[0]]
            s["noise_mask"] = samples["noise_mask"].repeat((amount, 1, 1, 1))
        if "batch_index" in s:
            offset = max(s["batch_index"]) - min(s["batch_index"]) + 1
            s["batch_index"] = s["batch_index"] + [x + (i * offset) for i in range(1, amount) for x in s["batch_index"]]
        return s

def upscale_latent(samples, scale_by=1.5, upscale_method="bilinear"):
    s = samples.copy()
    width = round(samples["samples"].shape[-1] * scale_by)
    height = round(samples["samples"].shape[-2] * scale_by)
    s["samples"] = comfy.utils.common_upscale(samples["samples"], width, height, upscale_method, "disabled")
    return s

def encode(vae, pixels):
    #Encode the image into latent space
    t = vae.encode(pixels[:,:,:,:3])
    return {"samples": t}

class UpscaleLatentBy1_5x:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "samples": ("LATENT",),
                              "amount": ("INT", {"default": 1, "min": 1, "max": 10}),
                              }}
    RETURN_TYPES = ("LATENT",)
    FUNCTION = "process"
    CATEGORY = "MzMaXaM"
    
    def process(self, samples, amount):
        return (repeat(upscale_latent(samples), amount),)
    
class UpscaleImageBy1_5x:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {   "pixels": ("IMAGE", ),
                                "vae": ("VAE", {"tooltip": "The VAE model used for decoding the latent."}),
                                "amount": ("INT", {"default": 1, "min": 1, "max": 10}),
                            }}
    RETURN_TYPES = ("LATENT",)
    FUNCTION = "process"
    CATEGORY = "MzMaXaM"

    def process(self, pixels, vae, amount):
        latent = encode(vae, pixels)
        upscaled_latent = upscale_latent(latent)
        return (repeat(upscaled_latent, amount),)

UBN_CLASS_MAPPINGS = {
    "UpscaleLatentBy1_5x": UpscaleLatentBy1_5x,
    "UpscaleImageBy1_5x": UpscaleImageBy1_5x,
}

UBN_NAME_MAPPINGS = {
    "UpscaleLatentBy1_5x": "Upscale Latent by 1.5x",
    "UpscaleImageBy1_5x": "Upscale Image by 1.5x",
}