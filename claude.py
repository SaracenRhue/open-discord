import anthropic
from typing import List, Dict, Any
from config import *

async def chat(messages: List[Dict[str, Any]]) -> str:
    """ Chat with a claude model. """
    client = anthropic.Anthropic(
        api_key=ANTHROPIC_API_KEY,
    )

    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=1000,
        temperature=0,
        messages=messages
    )
    return message.content[0].text

async def set_model(model: str) -> str:
    """ Set the model to use. """
    global CLAUDE_MODEL
    CLAUDE_MODEL = model
    return f'claude model set to {CLAUDE_MODEL}'