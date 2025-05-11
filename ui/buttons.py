import discord
import io
import asyncio
from utils.logger import logger


class ImageButtonView(discord.ui.View):
    def __init__(self, prompt: str):
        super().__init__(timeout=180)  # Таймаут - 3 минуты
        self.prompt = prompt

    @discord.ui.button(
            label="🔁 Regenerate", 
            style=discord.ButtonStyle.primary)
    async def regenerate_button(
        self, 
        interaction: discord.Interaction, 
        button: discord.ui.Button
        ):
        # Здесь можно реализовать логику повторной генерации изображения
        await interaction.response.defer(ephemeral=True)  # Сообщаем, что ответ придёт позже

        button.disabled = True
        await interaction.message.edit(view=self)
        await interaction.followup.send("⏳ Generating a new image, please wait...", ephemeral=True)

        logger.info("🔁 Regenerating image | Prompt: %s", self.prompt)
        start = asyncio.get_running_loop().time()

        # Получаем бота и HF-клиент через interaction.client
        bot = interaction.client
        hf_client = bot.hf_client

        try:
            # Выполняем генерацию в отдельном потоке, чтобы не блокировать event loop
            new_image = await asyncio.to_thread(
                hf_client.generate_image, self.prompt
                )
            duration = asyncio.get_running_loop().time() - start
            logger.info("✅ Image regenerated in %.2f sec | Prompt: %s", duration, self.prompt)

            # Сохраняем результат в буфер
            buf = io.BytesIO()
            new_image.save(buf, format="PNG")
            buf.seek(0)
            file = discord.File(fp=buf, filename="regenerated.png")

            button.disabled = False
            await interaction.message.edit(view=self)

            # Отправляем новое изображение
            await interaction.followup.send(
                content=f"{interaction.user.mention} Here is your regenerated image!\n**Prompt:** {self.prompt}", file=file
                )
        except Exception as e:
            logger.error("❌ Failed to regenerate image | Prompt: %s | Error: %s", self.prompt, str(e))
            await interaction.followup.send(
                f"It seems something went wrong while regenerating image: {e}"
                )