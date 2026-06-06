from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
from PIL import Image
import torch
import cv2
import os
import random
import numpy as np

# Load ControlNet model for structure guidance
controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/sd-controlnet-canny",
    torch_dtype=torch.float16
)

pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    controlnet=controlnet,
    torch_dtype=torch.float16
)

# ✅ Disable safety checker (THIS FIXES BLACK IMAGES)
pipe.safety_checker = None
pipe.requires_safety_checker = False

pipe = pipe.to("cuda")
pipe.enable_attention_slicing()

CT_FOLDER = "ct_slices"


def severity_text(score):
    if score < 25:
        return "healthy lung tissue with clear alveoli"
    elif score < 50:
        return "mild emphysema patterns and slight alveoli damage"
    elif score < 75:
        return "moderate emphysema with visible alveoli collapse and scarring"
    else:
        return "severe emphysema, collapsed alveoli, destroyed lung tissue and heavy scarring"


def load_random_ct():
    files = os.listdir(CT_FOLDER)
    path = os.path.join(CT_FOLDER, random.choice(files))
    return Image.open(path).convert("RGB")   # small fix


def ct_to_edges(ct_img):
    gray = cv2.cvtColor(np.array(ct_img), cv2.COLOR_RGB2GRAY)

    # ✅ Boost contrast so SD can see structure better
    gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)

    edges = cv2.Canny(gray, 60, 150)

    # ✅ Thicken edges (important for ControlNet)
    edges = cv2.dilate(edges, None)

    return Image.fromarray(edges)


def generate_lung_image(score):

    ct = load_random_ct()
    structure = ct_to_edges(ct)

    prompt = f"""
    highly realistic medical lung anatomy,
    internal tissue texture,
    based on CT scan structure,
    {severity_text(score)},
    clinical lighting,
    pathological accuracy,
    sharp focus,
    no artistic style
    """

    image = pipe(
        prompt,
        image=structure,
        num_inference_steps=30,
        guidance_scale=7.5,
        controlnet_conditioning_scale=0.8   # ✅ balance (important)
    ).images[0]

    image.save("../frontend/lung.png")
    save_grayscale(image)


def save_grayscale(image):
    gray = image.convert("L")
    gray.save("../frontend/lung_ct.png")
