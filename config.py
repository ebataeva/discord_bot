import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
HF_API_KEY = os.getenv("HF_API_KEY")
HF_MODEL_ENDPOINT = os.getenv("HF_MODEL_ENDPOINT", "https://api-inference.huggingface.co/models/your_model")