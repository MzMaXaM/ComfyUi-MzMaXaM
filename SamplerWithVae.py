import re
import math
import torch # type: ignore
import latent_preview # type: ignore
import comfy # type: ignore
from typing import Tuple, Dict

def common_ksampler(model, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent, denoise=1.0, disable_noise=False, start_step=None, last_step=None, force_full_denoise=False):
    latent_image = latent["samples"]
    latent_image = comfy.sample.fix_empty_latent_channels(model, latent_image)

    if disable_noise:
        noise = torch.zeros(latent_image.size(), dtype=latent_image.dtype, layout=latent_image.layout, device="cpu")
    else:
        batch_inds = latent["batch_index"] if "batch_index" in latent else None
        noise = comfy.sample.prepare_noise(latent_image, seed, batch_inds)

    noise_mask = None
    if "noise_mask" in latent:
        noise_mask = latent["noise_mask"]

    callback = latent_preview.prepare_callback(model, steps)
    disable_pbar = not comfy.utils.PROGRESS_BAR_ENABLED
    samples = comfy.sample.sample(model, noise, steps, cfg, sampler_name, scheduler, positive, negative, latent_image,
                                  denoise=denoise, disable_noise=disable_noise, start_step=start_step, last_step=last_step,
                                  force_full_denoise=force_full_denoise, noise_mask=noise_mask, callback=callback, disable_pbar=disable_pbar, seed=seed)
    out = latent_image.copy()
    out["samples"] = samples
    return (out, )

class KSamplerWithVAE:
    @classmethod
    def INPUT_TYPES(s):
        return {
            'required': {
                "model": ("MODEL", {"tooltip": "The model used for sampling."}),
                "seed": ("INT", {"tooltip": "The seed for random number generation."}),
                "steps": ("INT", {"tooltip": "The number of steps for sampling."}),
                "cfg": ("FLOAT", {"tooltip": "The classifier-free guidance scale."}),
                "sampler_name": (comfy.samplers.KSampler.SAMPLERS, {"tooltip": "The algorithm used when sampling, this can affect the quality, speed, and style of the generated output."}),
                "scheduler": (comfy.samplers.KSampler.SCHEDULERS, {"tooltip": "The scheduler controls how noise is gradually removed to form the image."}),
                "positive": ("CONDITIONING", {"tooltip": "The conditioning describing the attributes you want to include in the image."}),
                "negative": ("CONDITIONING", {"tooltip": "The conditioning describing the attributes you want to exclude from the image."}),
                "latent_image": ("LATENT", {"tooltip": "The latent image to denoise."}),
                "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01, "tooltip": "The amount of denoising applied, lower values will maintain the structure of the initial image allowing for image to image sampling."}),
                "vae": ("VAE", {"tooltip": "The VAE model used for decoding the latent."})
            }
        }

    RETURN_TYPES = ("LATENT", "IMAGE")
    OUTPUT_TOOLTIPS = ("The denoised latent.", "The decoded image.")
    FUNCTION = "sample_and_decode"

    CATEGORY = "MzMaXaM"
    DESCRIPTION = "Uses the provided model, positive and negative conditioning to denoise the latent image and then decodes it back into pixel space images."

    def sample_and_decode(self, model, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent_image, vae, denoise=1.0):
        disable_noise = False
        start_step = 0
        last_step = steps
        force_full_denoise = False

        latent_tensor = latent_image["samples"]
        latent_tensor = comfy.sample.fix_empty_latent_channels(model, latent_tensor)

        if disable_noise:
            noise = torch.zeros(latent_tensor.size(), dtype=latent_tensor.dtype, layout=latent_tensor.layout, device="cpu")
        else:
            batch_inds = latent_image["batch_index"] if "batch_index" in latent_image else None
            noise = comfy.sample.prepare_noise(latent_tensor, seed, batch_inds)

        noise_mask = None
        if "noise_mask" in latent_image:
            noise_mask = latent_image["noise_mask"]

        callback = latent_preview.prepare_callback(model, steps)
        disable_pbar = not comfy.utils.PROGRESS_BAR_ENABLED
        samples = comfy.sample.sample(model, noise, steps, cfg, sampler_name, scheduler, positive, negative, latent_tensor,
                                      denoise=denoise, disable_noise=disable_noise, start_step=start_step, last_step=last_step,
                                      force_full_denoise=force_full_denoise, noise_mask=noise_mask, callback=callback, disable_pbar=disable_pbar, seed=seed)
        out = latent_image.copy()
        out["samples"] = samples

        images = vae.decode(out["samples"])
        if len(images.shape) == 5: # Combine batches
            images = images.reshape(-1, images.shape[-3], images.shape[-2], images.shape[-1])
        return (out, images)

SWV_CLASS_MAPPINGS = {
    "KSamplerWithVAE": KSamplerWithVAE,
}

SWV_NAME_MAPPINGS = {
    "KSamplerWithVAE": "KSampler with VAE",
}