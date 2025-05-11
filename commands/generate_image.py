# commands/generate_image.py
import io
import discord
import asyncio
import time
from discord.ext import commands
from ui.buttons import ImageButtonView
from utils.logger import logger

@commands.command(name="generate")
async def generate_image_command(ctx, *, prompt: str):
    msg = await ctx.send("🖼 Generating image... please wait 1-2 minutes")
    start = time.time()
    logger.info("🧠 Starting image generation | Prompt: %s", prompt)
    try:
        image = await asyncio.to_thread(ctx.bot.hf_client.generate_image, prompt)
        logger.info("⏱ Image generated in %.2f sec | Prompt: %s", time.time() - start, prompt)
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        buf.seek(0)
        file = discord.File(fp=buf, filename="generated.png")

        # Pass the prompt to the View so the button can reuse it
        await msg.edit(content=f"{ctx.author.mention}\n**Prompt:** {prompt}", attachments=[file], view=ImageButtonView(prompt))
    except Exception as e:
        await msg.edit(content=f"❌ It seems something went wrong...: {e}")