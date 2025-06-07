import discord
from discord.ext import commands
from config import DISCORD_TOKEN
from commands.generate_image import generate_image_command, test_lido_prompts

from api.hf_client import HuggingFaceClient
from utils.logger import logger


intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix="!", intents=intents)
bot.hf_client = HuggingFaceClient()

# Регистрируем команду генерации изображения
bot.add_command(generate_image_command)
bot.add_command(test_lido_prompts)

@bot.event
async def on_ready():
    logger.info("✅ Bot is ready and logged in as %s", bot.user)

@bot.event
async def on_disconnect():
    logger.warning("⚠️ Bot has disconnected from Discord")

@bot.event
async def on_resumed():
    logger.info("🔄 Bot connection resumed")

bot.run(DISCORD_TOKEN)