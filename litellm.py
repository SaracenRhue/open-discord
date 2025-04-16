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
    response = client.models.list()
    models = [model.id for model in response.data]
    models = [f"{i}) {model}" for i, model in enumerate(models)]
    return '\n'.join(models)


async def chat(messages: List[Dict[str, Any]]) -> str:
    """ Chat with a gpt model. """
    client = openai.OpenAI(
        api_key="sk-uA0uTnd2IYPfWmME4_sF5A",
        base_url="http://192.168.178.132:4663"
    )

    completion = client.chat.completions.create(
        model=LITELLM_MODEL,
        messages=messages,
    )
    
    return completion.choices[0].message.content




# async def main():
#     test = await list_models()
#     print(test)


# asyncio.run(main())