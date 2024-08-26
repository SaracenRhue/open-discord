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

async def set_model(model):
    global MODEL
    MODEL = model
    return f'Model set to {MODEL}'

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
        # Run the image generation in the background
        image_task = asyncio.create_task(focus.txt2img(prompt))
        
        # Wait for the image generation to complete, with a timeout
        image = await asyncio.wait_for(image_task, timeout=120.0)  # 120 second timeout
        
        # Decode the base64 image and create a discord.File object
        image_bytes = base64.b64decode(image[0])
        file = discord.File(fp=io.BytesIO(image_bytes), filename="generated_image.png")
        
        # Send the generated image
        await interaction.followup.send(file=file)
        await interaction.followup.send(prompt)
    except asyncio.TimeoutError:
        await interaction.followup.send("Image generation timed out. Please try again.")
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {str(e)}")

## Ollama ##
# ollama list
@client.tree.command(name="ollama_list", description="List available models.")
async def ollama_list(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(await ollama.list())

# ollama run
@client.tree.command(name="ollama_run", description="Set the model to use.")
@app_commands.describe(model="The model to use.")
async def ollama_run(interaction: discord.Interaction, model: str) -> None:
    await interaction.response.send_message(await set_model(model))

# ollama pull
@client.tree.command(name="ollama_pull", description="Pull a model.")
@app_commands.describe(model="The model to pull.")
async def ollama_pull(interaction: discord.Interaction, model: str) -> None:
    await interaction.response.send_message(await ollama.pull(model))

# ollama rm
@client.tree.command(name="ollama_rm", description="Remove a model.")
@app_commands.describe(model="The model to remove.")
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
                    for i in range(0, len(final_response), 2000):
                        await message.channel.send(final_response[i:i+2000])
                else:
                    await message.channel.send(final_response)

            else:
                error_message = f"Failed to get response: {response.status}"
                await message.channel.send(error_message)


client.run(TOKEN)
