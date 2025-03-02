# commands/generate_image.py
import io
import discord
import asyncio
from discord.ext import commands
from ui.buttons import ImageButtonView

@commands.command(name="generate")
async def generate_image_command(ctx, *, prompt: str):
    await ctx.send("Генерирую изображение, подождите...")
    try:
        image = await asyncio.to_thread(ctx.bot.hf_client.generate_image, prompt)
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        buf.seek(0)
        file = discord.File(fp=buf, filename="generated.png")

        # Передаём промт в View, чтобы кнопка могла использовать тот же prompt
        await ctx.send(file=file, view=ImageButtonView(prompt))
    except Exception as e:
        await ctx.send(f"Произошла ошибка: {e}")