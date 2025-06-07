# commands/generate_image.py
import io
import discord
import asyncio
import time
from discord.ext import commands
from ui.buttons import ImageButtonView
from utils.logger import logger

def prepare_prompt(user_input: str) -> str:
    if "drop" in user_input.lower() or "droplet" in user_input.lower():
        return user_input
    else:
        return f"Centered Lido-style water droplet logo in foreground, in front of {user_input}, crypto branding, minimalistic, high contrast"

@commands.command(name="generate")
async def generate_image_command(ctx, *, prompt: str):
    msg = await ctx.send("🖼 Generating image... please wait 1-2 minutes")
    start = time.time()
    logger.info("🧠 Starting image generation | Prompt  : %s", prompt)
    prompt_droplet = prepare_prompt(prompt)
    try:
        image = await asyncio.to_thread(ctx.bot.hf_client.generate_image, prompt_droplet)
        logger.info("⏱ Image generated in %.2f sec | Prompt: %s", time.time() - start, prompt_droplet)
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        buf.seek(0)
        file = discord.File(fp=buf, filename="generated.png")

        # Pass the prompt to the View so the button can reuse it
        await msg.edit(content=f"{ctx.author.mention}\n**Prompt:** {prompt}", attachments=[file], view=ImageButtonView(prompt))
    except Exception as e:
        await msg.edit(content=f"❌ It seems something went wrong...: {e}")



# New command for testing multiple Lido-related prompts
@commands.command(name="test_lido_prompts")
async def test_lido_prompts(ctx):
    prompts = [
        "Lido-style water droplet, glossy, highly detailed, centered, minimal background",
        "Abstract Lido droplet, soft colors, smooth surface, futuristic design",
        "High quality Lido-style droplet, floating in white space, photorealistic",
        "Lido-themed droplet, stylized and sharp, 3D render, crypto-inspired",
        "Blue-green glowing droplet in Lido aesthetic, minimalism, digital art",
        "Lido droplet illustration, no text, centered, clean background"
    ]

    prompt_list_text = "\n".join([f"{i+1}. {p}" for i, p in enumerate(prompts)])
    await ctx.send(f"🧪 Testing multiple prompts... please wait\n\n**Prompt list:**\n{prompt_list_text}")

    for i, prompt in enumerate(prompts):
        msg = await ctx.send(f"🖼 Generating `{prompt}` ...")
        try:
            image = await asyncio.to_thread(ctx.bot.hf_client.generate_image, prompt)
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            buf.seek(0)
            file = discord.File(fp=buf, filename=f"prompt_{i + 1}.png")
            await msg.edit(content=f"✅ **Prompt {i+1}:** {prompt}", attachments=[file])
        except Exception as e:
            await msg.edit(content=f"❌ Failed for `{prompt}`: {e}")