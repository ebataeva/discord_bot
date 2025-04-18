import torch
from diffusers import DiffusionPipeline
from config import HF_API_KEY, HF_MODEL_ID

class HuggingFaceClient:
    def __init__(self):
        self.model_id = HF_MODEL_ID
        self.pipe = DiffusionPipeline.from_pretrained(
            self.model_id,
            torch_dtype=torch.float32,
            use_auth_token=HF_API_KEY  # передаём токен из .env
        )
        self.pipe.to("cpu")


    def generate_image(self, prompt: str):
        """
        Генерирует изображение по заданному промту.
        """
        image = self.pipe(
        prompt,
        height=512,
        width=512,
        num_inference_steps=45,
        guidance_scale=7.5
        ).images[0]
        return image