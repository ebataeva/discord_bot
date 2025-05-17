import torch
from diffusers import DiffusionPipeline
from config import HF_MODEL_ID

class HuggingFaceClient:
    def __init__(self):
        self.model_id = HF_MODEL_ID
        print(f"⚠️ LOADING MODEL: {self.model_id}")
        self.pipe = DiffusionPipeline.from_pretrained(
            self.model_id,
            torch_dtype=torch.float16,
            # local_files_only=True
        )
        self.pipe.to("cuda")


    def generate_image(self, prompt: str):
        """
        Генерирует изображение по заданному промту.
        """
        image = self.pipe(
        prompt,
        height=512,
        width=512,
        num_inference_steps=65,
        guidance_scale=6.5
        ).images[0]
        return image