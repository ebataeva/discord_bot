import discord

class ImageButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)  # Таймаут - 3 минуты

    @discord.ui.button(label="Перегенерировать", style=discord.ButtonStyle.primary)
    async def regenerate_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Здесь можно реализовать логику повторной генерации изображения
        await interaction.response.send_message("Кнопка перегенерации нажата!", ephemeral=True)