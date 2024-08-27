import aiohttp
import json
from config import OLLAMA_URL, MODEL

async def set_model(model):
    global MODEL
    MODEL = model
    return f'Model set to {MODEL}'

async def list():
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{OLLAMA_URL}/api/tags') as resp:
            data = await resp.json()
            return '\n'.join([model['name'] for model in data['models']])


async def pull(model):
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{OLLAMA_URL}/api/pull', json={'name': model}) as resp:
            data = await resp.json()
            return data['message']
        
async def rm(model):
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{OLLAMA_URL}/api/rm', json={'name': model}) as resp:
            data = await resp.json()
            return data['message']
        

async def run(model):
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{OLLAMA_URL}/api/run', json={'name': model}) as resp:
            data = await resp.json()
            return data['message']

async def chat(messages):
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{OLLAMA_URL}/api/chat', json={'model': MODEL, 'messages': messages, 'stream': True}) as response:
            if response.status == 200:
                response_texts = []
                async for line in response.content:
                    if line:
                        data = json.loads(line.decode('utf-8'))
                        if 'message' in data:
                            response_text = data['message'].get('content', '')
                            response_texts.append(response_text)
                # Join all response texts into a single string
                final_response = ''.join(response_texts)
                return final_response
            else:
                return f"Error: {response.status}"