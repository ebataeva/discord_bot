
# commands/generate_image.py
import io
import discord
import asyncio
import time
from discord.ext import commands
from ui.buttons import ImageButtonView
from utils.logger import logger

async def generate_images_from_prompt_list(ctx, prompts: list, prefix: str, description: str):
    prompt_list_text = "\n".join([f"{i+1}. {p}" for i, p in enumerate(prompts)])
    await ctx.send(f"🧪 {description}\n\n**Prompt list:**\n{prompt_list_text}")

    for i, prompt in enumerate(prompts):
        msg = await ctx.send(f"🖼 Generating `{prompt}` ...")
        try:
            image = await asyncio.to_thread(ctx.bot.hf_client.generate_image, prompt)
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            buf.seek(0)
            file = discord.File(fp=buf, filename=f"{prefix}_{i + 1}.png")
            await msg.edit(content=f"✅ **Prompt {i+1}:** {prompt}", attachments=[file])
        except Exception as e:
            await msg.edit(content=f"❌ Failed for `{prompt}`: {e}")

def prepare_prompt(user_input: str) -> str:
    if "drop" in user_input.lower() or "droplet" in user_input.lower():
        return user_input
    else:
        return f"{user_input}, with subtle Lido-style water droplet elements integrated in the background, high quality, balanced composition"

@commands.command(name="generate")
async def generate_image_command(ctx, *, prompt: str):
    msg = await ctx.send("🖼 Generating image... please wait a bit...")
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


@commands.command(name="combine_with_lido")
async def combine_with_lido(ctx, *, user_input: str):
    lido_addons = [
        "in a room decorated with Lido-style water droplets, high detail, bright colors",
        "with a glowing Lido-style water droplet nearby, photorealistic, sharp details, happy mood",
        "with Lido-inspired droplets subtly in the design, high quality, realistic",
        "under a Lido-style rain of blue glowing droplets, cinematic lighting, ultra-realistic",
        "surrounded by Lido-themed elements, droplets in background, vibrant digital art",
        "inside a glowing Lido droplet, fantasy setting, detailed and soft lighting"
    ]

    prompts = [f"{user_input}, {addon}" for addon in lido_addons]

    await generate_images_from_prompt_list(ctx, prompts, "lido", "Testing your input combined with Lido aesthetics")

@commands.command(name="combine_with_big_droplet")
async def combine_with_big_droplet(ctx, *, user_input: str):
    
    big_droplet_addons = [
        "with a huge glossy Lido-style droplet in the center, highly detailed, reflecting light",
        "featuring one large glowing water droplet, Lido-style, with shiny surface and reflections",
        "dominated by a single big crystal-like Lido droplet, luminous, photorealistic",
        "with one oversized sparkling droplet hovering in the air, digital art style",
        "a scene with one prominent glossy blue Lido droplet, surreal lighting, beautiful reflections",
        "with an enormous water droplet as the centerpiece, shining like a gem, cinematic composition"
    ]

    prompts = [f"{user_input}, {addon}" for addon in big_droplet_addons]

    await generate_images_from_prompt_list(ctx, prompts, "big_droplet", "Combining your input with BIG droplet aesthetics")
@commands.command(name="combine_with_tech_droplets")
async def combine_with_tech_droplets(ctx, *, user_input: str):
    tech_addons = [
        "with glowing digital Lido droplets, tech-inspired UI elements, cyberpunk background",
        "featuring a large neon-blue droplet with circuitry inside, futuristic setting, sci-fi lighting",
        "surrounded by holographic droplet projections, digital rain, cyberpunk cityscape",
        "one central Lido droplet containing a microchip, blue and violet glow, tech aesthetics",
        "Lido droplet embedded in a digital HUD interface, clean lines, high-tech UI overlay",
        "floating above a grid with shiny cyber droplets falling, stylized, digital art"
    ]

    prompts = [f"{user_input}, {addon}" for addon in tech_addons]
    await generate_images_from_prompt_list(ctx, prompts, "tech_droplet", "Combining your input with TECH droplet aesthetics")


@commands.command(name="combine_with_abstract_droplets")
async def combine_with_abstract_droplets(ctx, *, user_input: str):
    abstract_addons = [
        "with abstract liquid droplet forms, surreal background, bold artistic shapes",
        "inside a giant translucent droplet, warped reflections, dreamlike colors",
        "surrounded by floating symbolic droplets, geometric fragments, digital painting",
        "the entire scene contained within a single large Lido-style droplet, reflective surface, artistic composition",
        "featuring melting droplet patterns, distorted light, vivid surrealism",
        "a warped reality held inside a glossy Lido droplet, modern abstract art style"
    ]

    prompts = [f"{user_input}, {addon}" for addon in abstract_addons]
    await generate_images_from_prompt_list(ctx, prompts, "abstract_droplet", "Combining your input with ABSTRACT droplet aesthetics")

 @commands.command(name="combine_inside_droplet")
 async def combine_inside_droplet(ctx, *, user_input: str):
     inside_droplet_addons = [
         "the scene is encapsulated inside a transparent water droplet, fisheye distortion, high detail, surreal lighting",
         "everything is happening inside one giant Lido droplet, the curved surface warps the world inside, cinematic effect",
         "the entire world is seen through a large glossy droplet lens, bluish tones, glowing edges, dreamy effect",
         "immersed inside a droplet bubble, refracted light and reflections shape the environment, crystal-clear",
         "a magical world inside a shiny Lido-style droplet, warped interior, smooth reflections",
         "dreamlike environment seen from within a droplet shell, curvature and glow, hyper-realistic art"
     ]
     prompts = [f"{user_input}, {addon}" for addon in inside_droplet_addons]
     await generate_images_from_prompt_list(ctx, prompts, "inside_droplet", "Generating scenes INSIDE a droplet")