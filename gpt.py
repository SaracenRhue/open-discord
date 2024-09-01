from openai import OpenAI
from typing import List, Dict, Any

async def chat(messages: List[Dict[str, Any]]) -> str:
    """ Chat with a gpt model. """
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )
    
    return completion.choices[0].message.content

async def list() -> str:
    """ List available models. """
    client = OpenAI()
    models_page = client.models.list()
    model_ids = [model.id for model in models_page]
    return '\n'.join(model_ids)

async def set_model(model: str) -> str:
    """ Set the model to use. """
    global GPT_MODEL
    GPT_MODEL = model
    return f'gpt model set to {GPT_MODEL}'