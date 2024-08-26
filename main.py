import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import json
import base64
import io
import asyncio
from config import *
import focus
import ollama

# Create a new client instance
intents = discord.Intents.all()
client = commands.Bot(command_prefix="/", intents=intents)
tree = client.tree

## Focus ##
# focus txt2img
@client.tree.command(name="sd", description="Generate an image from a prompt.")
async def sd(interaction: discord.Interaction, prompt: str) -> None:
    # Acknowledge the interaction immediately
    await interaction.response.defer(thinking=True)
    
    try:
        for _ in range(SD_BATCH_COUNT):
            # Run the image generation in the background
            image_task = asyncio.create_task(focus.txt2img(prompt))

            # Wait for the image generation to complete, with a timeout
            images = await asyncio.wait_for(image_task, timeout=120.0)  # 120 second timeout

            for image in images:
                # Decode the base64 image and create a discord.File object
                image_bytes = base64.b64decode(image)
                file = discord.File(fp=io.BytesIO(image_bytes), filename="generated_image.png")
                # Send the generated image
                await interaction.followup.send(file=file)

        await interaction.followup.send(prompt)
    except asyncio.TimeoutError:
        await interaction.followup.send("Image generation timed out. Please try again.")
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {str(e)}")


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

    # Preparing the payload for the HTTP request
    payload = {
        "model": MODEL,
        "messages": conversation_history[message.channel.id],
        "stream": True  # Ensure that we handle streaming
    }

    # Asynchronous HTTP POST request to Ollama
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{OLLAMA_URL}/api/chat', json=payload) as response:
            if response.status == 200:
                response_texts = []
                async for line in response.content:
                    if line:
                        data = json.loads(line.decode('utf-8'))
                        if 'message' in data:
                            response_text = data['message'].get('content', '')
                            response_texts.append(response_text)
                            # Append the assistant's message to the conversation history
                            conversation_history[message.channel.id].append({"role": "assistant", "content": response_text})

                # Join all response texts into a single string
                final_response = ''.join(response_texts)
                
                # Split the response if it exceeds Discord's character limit
                if len(final_response) > 2000:
                    chunks = []
                    current_chunk = ""
                    code_block = False
                    code_block_lang = ""
                    lines = final_response.split('\n')

                    for line in lines:
                        if line.strip().startswith('```'):
                            if not code_block:
                                code_block = True
                                code_block_lang = line.strip()[3:].strip()
                            else:
                                code_block = False

                        if len(current_chunk) + len(line) + 1 > 2000:
                            if code_block:
                                current_chunk += '```\n'
                            chunks.append(current_chunk.strip())
                            current_chunk = ""
                            if code_block:
                                current_chunk += f'```{code_block_lang}\n'

                        current_chunk += line + '\n'

                    if current_chunk:
                        chunks.append(current_chunk.strip())

                    for chunk in chunks:
                        await message.channel.send(chunk)
                else:
                    await message.channel.send(final_response)
            else:
                await message.channel.send(f"Error: {response.status}")

client.run(TOKEN)
