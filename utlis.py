from config import *
import discord
import base64
import io
import asyncio
import focus

async def format_response(text):
    if len(text) > 2000:
        chunks = []
        current_chunk = ""
        code_block = False
        code_block_lang = ""
        lines = text.split('\n')

        for line in lines:
            if line.strip().startswith('```'):
                if not code_block:
                    code_block = True
                    code_block_lang = line.strip()[3:].strip()
                else:
                    code_block = False

            if len(current_chunk) + len(line) + 1 > 2000:
                if code_block:
                    current_chunk += '```\n'
                chunks.append(current_chunk.strip())
                current_chunk = ""
                if code_block:
                    current_chunk += f'```{code_block_lang}\n'

            current_chunk += line + '\n'

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks
    else:
        return [text]
    

async def generate_and_send_images(interaction: discord.Interaction, prompt: str):
    global SD_PROMPT
    SD_PROMPT = prompt

    try:
        for _ in range(SD_BATCH_COUNT):
            image_task = asyncio.create_task(focus.txt2img(SD_PROMPT))
            images = await asyncio.wait_for(image_task, timeout=120.0)

            for image in images:
                image_bytes = base64.b64decode(image)
                file = discord.File(fp=io.BytesIO(image_bytes), filename="generated_image.png")
                await interaction.followup.send(file=file)

        await interaction.followup.send(f"Prompt used: \n ```\n{SD_PROMPT}\n```")

    except asyncio.TimeoutError:
        await interaction.followup.send("Image generation timed out. Please try again.")
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {str(e)}")