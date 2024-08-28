import aiohttp
import json
from typing import Dict, List, Any
from config import *

async def set_model(model):
    global MODEL
    MODEL = model
    return f'Model set to {MODEL}'

async def request(method: str, endpoint: str, **kwargs) -> Any:
    """ Make a request to the Ollama API. """
    url = f"{OLLAMA_URL}/api/{endpoint.lstrip('/')}"
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, **kwargs) as response:
            if response.status == 200:
                return await response.json()
            else:
                return {"error": f"Error: {response.status}"}

async def list() -> str:
    """ List available models. """
    data = await request("GET", "tags")
    return '\n'.join([model['name'] for model in data['models']])

async def pull(model: str) -> str:
    """ Pull a model. """
    data = await request("POST", "pull", json={'name': model})
    return data['message']

async def rm(model: str) -> str:
    """ Remove a model. """
    data = await request("POST", "rm", json={'name': model})
    return data['message']

async def run(model: str) -> str:
    """ Run a model. """
    data = await request("POST", "run", json={'name': model})
    return data['message']

async def chat(messages: List[Dict[str, Any]]) -> str:
    """ Chat with a model. """
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