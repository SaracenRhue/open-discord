from config import *
import discord
import base64
import io
import asyncio
import focus

def format_response(text: str) -> list[str]:
    """ Format the response text to fit within 2000 characters and handle code blocks. """
    if len(text) <= 2000:
        return [text]
    
    chunks = []
    current_chunk = ""
    code_block = False
    code_block_lang = ""
    
    # Pre-split lines for efficiency
    lines = text.split('\n')
    
    for line in lines:
        line_stripped = line.strip()
        
        # Handle code block markers
        if line_stripped.startswith('```'):
            if not code_block:
                code_block = True
                code_block_lang = line_stripped[3:].strip()
            else:
                code_block = False

        # Check if adding this line would exceed limit
        new_length = len(current_chunk) + len(line) + 1
        if new_length > 2000:
            # Close code block if needed
            if code_block:
                current_chunk += '```'
            
            # Add chunk if it has content
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            
            # Start new chunk
            current_chunk = ""
            if code_block:
                current_chunk = f'```{code_block_lang}\n'

        current_chunk += line + '\n'

    # Add final chunk if it has content
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks
    

async def generate_and_send_images(interaction: discord.Interaction, prompt: str) -> None:
    """ Generate and send images based on the prompt. """
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

# async def get_config() -> str:
#     """ Get all config variables. """


    