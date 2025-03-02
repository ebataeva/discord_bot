# api/huggingface_api.py
import torch
from diffusers import DiffusionPipeline
from config import HF_API_KEY, HF_MODEL_ENDPOINT

class HuggingFaceClient:
    def __init__(self):
        # Задайте id модели; позже, если захотите поменять модель, достаточно будет изменить эту переменную
        # self.model_id = "stabilityai/stable-diffusion-2"
        self.model_id = "runwayml/stable-diffusion-v1-5"
        # Загружаем пайплайн с использованием float32 (на CPU работают операции с этим типом)
        self.pipe = DiffusionPipeline.from_pretrained(
            self.model_id,
            torch_dtype=torch.float32,
            use_auth_token=HF_API_KEY  # передаём токен из .env
        )
        # Переносим модель на CPU, так как GPU отсутствует
        self.pipe.to("cpu")


    def generate_image(self, prompt: str):
        """
        Генерирует изображение по заданному промту.
        """
        image = self.pipe(
        prompt,
        height=512,
        width=512,
        num_inference_steps=10,
        guidance_scale=7.5
        ).images[0]
        return image