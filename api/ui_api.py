import replicate
from config import REPLICATE_API_TOKEN 
class ReplicateClient:
    def __init__(self):
              self.model = replicate.models.get("stabilityai/stable-diffusion")
    
    def generate_image(self, prompt: str):
        
        output = self.model.predict(prompt=prompt, num_inference_steps=50)
        return output