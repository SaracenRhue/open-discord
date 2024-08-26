from config import TOKEN, ADMIN_ID, OLLAMA_URL, MODEL
import asyncio
import ollama

async def main():
	msg = await ollama.chat("Hello, how are you?") 
	print(msg)

asyncio.run(main())