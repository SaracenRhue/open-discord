import discord
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



async def commands(message):
    message = message.content.lower()
    if message.startswith('#help'):
        response = 'some response text'
    elif message.startswith('#list'):
        response = await ollama_list()  
    elif message.startswith('#run'):
        response = await set_model(message.split('#run ')[1])
    elif message.startswith('#pull'):
        response = await ollama_pull(message.split('#pull ')[1])
    elif message.startswith('#rm'):
        response = await ollama_rm(message.split('#rm ')[1])
    return response

client = discord.Client(intents=discord.Intents.default())

# Dictionary to store conversation history for each channel
conversation_history = {}

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('#'):
        command_response = await commands(message)
        await message.channel.send(command_response)
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
                if response_texts:
                    await message.channel.send(''.join(response_texts))
                else:
                    await message.channel.send('No response received.')
            else:
                error_message = f"Failed to get response: {response.status}"
                await message.channel.send(error_message)

client.run(TOKEN)
