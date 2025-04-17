import discord
import io
import asyncio



class ImageButtonView(discord.ui.View):
    def __init__(self, prompt: str):
        super().__init__(timeout=180)  # Таймаут - 3 минуты
        self.prompt = prompt

    @discord.ui.button(
            label="Try ones more!", 
            style=discord.ButtonStyle.primary)
    async def regenerate_button(
        self, 
        interaction: discord.Interaction, 
        button: discord.ui.Button
        ):
        # Здесь можно реализовать логику повторной генерации изображения
        await interaction.response.defer(ephemeral=True)  # Сообщаем, что ответ придёт позже

        # Получаем бота и HF-клиент через interaction.client
        bot = interaction.client
        hf_client = bot.hf_client

        try:
            # Выполняем генерацию в отдельном потоке, чтобы не блокировать event loop
            new_image = await asyncio.to_thread(
                hf_client.generate_image, self.prompt
                )

            # Сохраняем результат в буфер
            buf = io.BytesIO()
            new_image.save(buf, format="PNG")
            buf.seek(0)
            file = discord.File(fp=buf, filename="regenerated.png")

            # Отправляем новое изображение
            await interaction.followup.send(
                "Here is new image!", file=file
                )
        except Exception as e:
            await interaction.followup.send(
                f"It seems something went wrong while regenerating image: {e}"
                )