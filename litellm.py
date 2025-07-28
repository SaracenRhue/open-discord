import openai
import asyncio
import aiohttp
import json
from typing import List, Dict, Any
from config import *

# Keep the sync client for model listing (used less frequently)
client = openai.OpenAI(
    api_key="sk-uA0uTnd2IYPfWmME4_sF5A",
    base_url="http://192.168.178.132:4663"
)

# Create persistent session for async requests
_session = None

async def get_session():
    global _session
    if _session is None or _session.closed:
        connector = aiohttp.TCPConnector(
            limit=10,  # Max connections
            limit_per_host=5,  # Max connections per host
            keepalive_timeout=30,  # Keep connections alive
            enable_cleanup_closed=True,
            use_dns_cache=True,  # Cache DNS lookups
            ttl_dns_cache=300  # DNS cache TTL
        )
        timeout = aiohttp.ClientTimeout(total=120, connect=10)
        _session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={
                "Authorization": "Bearer sk-uA0uTnd2IYPfWmME4_sF5A",
                "Content-Type": "application/json"
            }
        )
    return _session

async def cleanup_session():
    """Cleanup the session when shutting down."""
    global _session
    if _session and not _session.closed:
        await _session.close()

async def set_model(model) -> str:
    """ Set the model to use. """
    global LITELLM_MODEL
    models = await list_models()
    try:
        model = int(model)  
        LITELLM_MODEL = models.split('\n')[int(model)].split(') ')[1]
        return f'Model set to {LITELLM_MODEL}'
    except: 
        pass
    
    if model not in models.split('\n'):
        return f'Model {model} not found.'
    else:
        LITELLM_MODEL = model
        return f'Model set to {LITELLM_MODEL}'

# async def request(modelname: str, message: str):
#     """ Request a response from the model.  """
#     response = client.chat.completions.create(
#         model=modelname,
#         messages=[{"role": "user", "content": message}],
#         # stream=True
#     )
#     return response.choices[0].message.content

async def list_models():
    """ List available models. """
    def _list_models_sync():
        response = client.models.list()
        models = [model.id for model in response.data]
        models = [f"{i}) {model}" for i, model in enumerate(models)]
        return '\n'.join(models)
    
    try:
        return await asyncio.wait_for(
            asyncio.to_thread(_list_models_sync),
            timeout=30.0  # 30 second timeout
        )
    except asyncio.TimeoutError:
        return "Error: Request timed out while fetching models"
    except Exception as e:
        return f"Error fetching models: {str(e)}"


async def chat(messages: List[Dict[str, Any]]) -> str:
    """ Chat with a gpt model using async HTTP for better performance. """
    try:
        session = await get_session()
        
        payload = {
            "model": LITELLM_MODEL,
            "messages": messages,
        }
        
        async with session.post(
            "http://192.168.178.132:4663/v1/chat/completions",
            json=payload
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data["choices"][0]["message"]["content"]
            else:
                error_text = await response.text()
                return f"Error: HTTP {response.status} - {error_text}"
                
    except asyncio.TimeoutError:
        return "Sorry, the request timed out. Please try again with a shorter message or check if the LLM service is responding."
    except Exception as e:
        return f"Error: {str(e)}"




# async def main():
#     test = await list_models()
#     print(test)


# asyncio.run(main())