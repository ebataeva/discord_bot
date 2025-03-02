import io
import discord
import asyncio
from discord.ext import commands
from ui.buttons import ImageButtonView  # Импортируем класс кнопок


@commands.command(name="generate")
async def generate_image_command(ctx, *, prompt: str):
    await ctx.send("Генерирую изображение, подождите...")
    try:
        # Используем уже инициализированный экземпляр из bot.hf_client
        image = await asyncio.to_thread(ctx.bot.hf_client.generate_image, prompt)
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        buf.seek(0)
        file = discord.File(fp=buf, filename="generated.png")
        await ctx.send(file=file, view=ImageButtonView())
    except Exception as e:
        await ctx.send(f"Произошла ошибка: {e}")