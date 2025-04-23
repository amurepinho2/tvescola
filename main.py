from diffusers import StableDiffusionPipeline
import torch

# Corrigido: dummy_checker deve retornar lista
def dummy_checker(images, **kwargs):
    return images, [False] * len(images)

pipe = StableDiffusionPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4",
    torch_dtype=torch.float16,
    safety_checker=dummy_checker  # desativa o filtro NSFW corretamente
)
pipe = pipe.to("mps")

prompt = "Minimalist white flat icon of a molecule on a green gradient background, no text, centered"
image = pipe(prompt).images[0]
image.save("bioquimica_degrade.png")
