import discord
import aiohttp
import os

# Environment variables for tokens and keys
TOKEN = os.getenv('DISCORD_TOKEN')
ADMIN = os.getenv('ADMIN_ID')
OPEN_WEBUI_URL = os.getenv('OPEN_WEBUI_URL')
OPEN_WEBUI_KEY = os.getenv('OPEN_WEBUI_KEY')
MODEL= os.getenv('MODEL')

# Constructing the full API endpoint
OPEN_WEBUI_ENTRY = OPEN_WEBUI_URL + '/ollama/api/generate'

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
    # Preparing the headers and payload for the HTTP request
        headers = {
            'Authorization': f'Bearer {OPEN_WEBUI_KEY}',
            'Content-Type': 'application/json'
        }
        payload = {
            'model': 'llama3',  # Or any other model you want to specify
            'prompt': message.content,
            'stream': False
        }

        # Asynchronous HTTP POST request to the OpenWebUI
        async with aiohttp.ClientSession() as session:
            async with session.post(OPEN_WEBUI_ENTRY, json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    response_text = data.get('response', 'No response received.')
                    await message.channel.send(response_text)
                else:
                    error_message = f"Failed to get response: {response.status}"
                    await message.channel.send(error_message)

client.run(TOKEN)
