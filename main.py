import discord
from discord.ext import commands
import aiohttp
import json
import base64
import io
import asyncio
from config import *
import focus
import ollama
import utlis

# Create a new client instance
intents = discord.Intents.all()
client = commands.Bot(command_prefix="/", intents=intents)
tree = client.tree

## Focus ##
# focus txt2img
async def generate_and_send_images(interaction: discord.Interaction, prompt: str):
    global SD_PROMPT
    SD_PROMPT = prompt

    try:
        for _ in range(SD_BATCH_COUNT):
            image_task = asyncio.create_task(focus.txt2img(SD_PROMPT))
            images = await asyncio.wait_for(image_task, timeout=120.0)

            for image in images:
                image_bytes = base64.b64decode(image)
                file = discord.File(fp=io.BytesIO(image_bytes), filename="generated_image.png")
                await interaction.followup.send(file=file)

        await interaction.followup.send(f"Prompt used: \n ```\n{SD_PROMPT}\n```")

    except asyncio.TimeoutError:
        await interaction.followup.send("Image generation timed out. Please try again.")
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {str(e)}")

@client.tree.command(name="sd", description="Generate an image from a prompt.")
async def sd(interaction: discord.Interaction, prompt: str) -> None:
    await interaction.response.defer(thinking=True)
    await generate_and_send_images(interaction, prompt)

@client.tree.command(name="sd_rerun", description="Generate an image from the last prompt.")
async def sd_rerun(interaction: discord.Interaction) -> None:
    await interaction.response.defer(thinking=True)
    if SD_PROMPT:
        await generate_and_send_images(interaction, SD_PROMPT)
    else:
        await interaction.followup.send("No previous prompt found. Please use /sd first.")

# focus set width
@client.tree.command(name="sd_width", description="Set the width.")
async def set_width(interaction: discord.Interaction, width: int) -> None:
    await interaction.response.send_message(await focus.set_width(width))
# focus set height
@client.tree.command(name="sd_height", description="Set the height.")
async def set_height(interaction: discord.Interaction, height: int) -> None:
    await interaction.response.send_message(await focus.set_height(height))

# focus set steps
@client.tree.command(name="sd_steps", description="Set the number of steps.")
async def set_steps(interaction: discord.Interaction, steps: int) -> None:
    await interaction.response.send_message(await focus.set_steps(steps))

# focus set cfg scale
@client.tree.command(name="sd_cfg_scale", description="Set the cfg scale.")
async def set_cfg_scale(interaction: discord.Interaction, cfg_scale: float) -> None:
    await interaction.response.send_message(await focus.set_cfg_scale(cfg_scale))

# focus set batch count
@client.tree.command(name="sd_batch_count", description="Set the batch count.")
async def set_batch_count(interaction: discord.Interaction, batch_count: int) -> None:
    await interaction.response.send_message(await focus.set_batch_count(batch_count))

# focus set batch size
@client.tree.command(name="sd_batch_size", description="Set the batch size.")
async def set_batch_size(interaction: discord.Interaction, batch_size: int) -> None:
    await interaction.response.send_message(await focus.set_batch_size(batch_size))

# focus list models
@client.tree.command(name="sd_list_models", description="List available models.")
async def list_models(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(await focus.list_models())
## Ollama ##
# ollama list
@client.tree.command(name="ollama_list", description="List available models.")
async def ollama_list(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(await ollama.list())

# ollama run
@client.tree.command(name="ollama_run", description="Set the model to use.")
async def ollama_run(interaction: discord.Interaction, model: str) -> None:
    await interaction.response.send_message(await ollama.set_model(model))

# ollama pull
@client.tree.command(name="ollama_pull", description="Pull a model.")
async def ollama_pull(interaction: discord.Interaction, model: str) -> None:
    await interaction.response.send_message(await ollama.pull(model))

# ollama rm
@client.tree.command(name="ollama_rm", description="Remove a model.")
async def ollama_rm(interaction: discord.Interaction, model: str) -> None:
    await interaction.response.send_message(await ollama.rm(model))
    
# Dictionary to store conversation history for each channel
conversation_history = {}

@client.event
async def on_ready():
    await client.tree.sync()
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Initialize conversation history for the channel if it doesn't exist
    if message.channel.id not in conversation_history:
        conversation_history[message.channel.id] = []

    # Append the user's message to the conversation history
    conversation_history[message.channel.id].append({"role": "user", "content": message.content})
    # Send chat request to Ollama
    response = await ollama.chat(conversation_history[message.channel.id])
    # Append the model's response to the conversation history
    conversation_history[message.channel.id].append({"role": "assistant", "content": response})
    # Split the response if it exceeds Discord's character limit
    for chunk in await utlis.format_response(response):
        await message.channel.send(chunk)

client.run(TOKEN)