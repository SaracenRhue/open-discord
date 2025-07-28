import openai
import asyncio
from typing import List, Dict, Any
from config import *

client = openai.OpenAI(
    api_key="sk-uA0uTnd2IYPfWmME4_sF5A",
    base_url="http://192.168.178.132:4663"
)

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
    """ Chat with a gpt model. """
    def _chat_sync():
        completion = client.chat.completions.create(
            model=LITELLM_MODEL,
            messages=messages,
        )
        return completion.choices[0].message.content
    
    try:
        # Run the synchronous OpenAI call in a thread pool with timeout
        return await asyncio.wait_for(
            asyncio.to_thread(_chat_sync),
            timeout=120.0  # 60 second timeout
        )
    except asyncio.TimeoutError:
        return "Sorry, the request timed out. Please try again with a shorter message or check if the LLM service is responding."
    except Exception as e:
        return f"Error: {str(e)}"




# async def main():
#     test = await list_models()
#     print(test)


# asyncio.run(main())