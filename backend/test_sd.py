from diffusers import StableDiffusionPipeline
import torch

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
)

pipe = pipe.to("cuda")

prompt = "realistic medical illustration of human lungs with severe smoking damage"

image = pipe(prompt).images[0]

image.save("lung_local.png")

print("Image generated!")
