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