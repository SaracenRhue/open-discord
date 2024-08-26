import discord
from discord.ext import commands
from discord import app_commands
import os
import aiohttp
import json

# Load environment variables from .env file if it exists
env = {}
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        for line in f:
            key, value = line.strip().split('=')
            env[key] = value
else:
    env['DISCORD_TOKEN'] = os.getenv('DISCORD_TOKEN')
    env['ADMIN_ID'] = os.getenv('ADMIN_ID')
    env['OLLAMA_URL'] = os.getenv('OLLAMA_URL')
    env['MODEL'] = os.getenv('MODEL')

TOKEN = env['DISCORD_TOKEN']
ADMIN_ID = env['ADMIN_ID']
OLLAMA_URL = env['OLLAMA_URL']
MODEL = env['MODEL']


async def ollama_list():
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{OLLAMA_URL}/api/tags') as resp:
            data = await resp.json()
            return '\n'.join([model['name'] for model in data['models']])

async def set_model(model):
    global MODEL
    MODEL = model
    return f'Model set to {MODEL}'

async def ollama_pull(model):
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{OLLAMA_URL}/api/pull', json={'name': model}) as resp:
            data = await resp.json()
            return data['message']
        
async def ollama_rm(model):
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{OLLAMA_URL}/api/rm', json={'name': model}) as resp:
            data = await resp.json()
            return data['message']

# Create a new client instance
intents = discord.Intents.all()
client = commands.Bot(command_prefix="/", intents=intents)
tree = client.tree


# ollama list
@client.tree.command(name="ollama_list", description="List available models.")
async def ollama_list_cmd(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(await ollama_list())

# ollama run
@client.tree.command(name="ollama_run", description="Set the model to use.")
@app_commands.describe(model="The model to use.")
async def ollama_run_cmd(interaction: discord.Interaction, model: str) -> None:
    await interaction.response.send_message(await set_model(model))

# ollama pull
@client.tree.command(name="ollama_pull", description="Pull a model.")
@app_commands.describe(model="The model to pull.")
async def ollama_pull_cmd(interaction: discord.Interaction, model: str) -> None:
    await interaction.response.send_message(await ollama_pull(model))

# ollama rm
@client.tree.command(name="ollama_rm", description="Remove a model.")
@app_commands.describe(model="The model to remove.")
async def ollama_rm_cmd(interaction: discord.Interaction, model: str) -> None:
    await interaction.response.send_message(await ollama_rm(model))
# Dictionary to store conversation history for each channel
conversation_history = {}

@client.event
async def on_ready():
    await client.tree.sync()
    print(f'We have logged in as {client.user}')

# Dictionary to store conversation history for each channel
conversation_history = {}

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
