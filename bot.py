import discord
from discord.ext import commands
from config import DISCORD_TOKEN
from commands.generate_image import generate_image_command

from api.ui_api import HuggingFaceClient


intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix="!", intents=intents)
bot.hf_client = HuggingFaceClient()

# Регистрируем команду генерации изображения
bot.add_command(generate_image_command)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.run(DISCORD_TOKEN)