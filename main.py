import discord
from discord.ext import commands
from config import *
import focus
import ollama
import gpt
import utlis

# Create a new client instance
intents = discord.Intents.all()
client = commands.Bot(command_prefix="/", intents=intents)
tree = client.tree

# Dictionary to store conversation history for each channel
conversation_history = {}

@client.tree.command(name="use_ollama", description="Set LM provider to Ollama.")
async def use_ollama(interaction: discord.Interaction) -> None:
    global LM_PROVIDER
    LM_PROVIDER = "ollama"
    await interaction.response.send_message("LM provider set to Ollama.")

@client.tree.command(name="use_gpt", description="Set LM provider to GPT.")
async def use_gpt(interaction: discord.Interaction) -> None:
    global LM_PROVIDER
    LM_PROVIDER = "gpt"
    await interaction.response.send_message("LM provider set to GPT.")


## Focus ##
# focus txt2img
@client.tree.command(name="sd", description="Generate an image from a prompt.")
async def sd(interaction: discord.Interaction, prompt: str) -> None:
    await interaction.response.defer(thinking=True)
    await utlis.generate_and_send_images(interaction, prompt)

@client.tree.command(name="sd_rerun", description="Generate an image from the last prompt.")
async def sd_rerun(interaction: discord.Interaction) -> None:
    await interaction.response.defer(thinking=True)
    if SD_PROMPT:
        await utlis.generate_and_send_images(interaction, SD_PROMPT)
    else:
        await interaction.followup.send("No previous prompt found. Please use /sd first.")

# focus set width
@client.tree.command(name="sd_width", description="Set the width.")
async def set_width(interaction: discord.Interaction, width: int) -> None:
    await interaction.response.send_message(await focus.set_width(width))
# focus set height
@client.tree.command(name="sd_height", description="Set the height.")
async def set_height(interaction: discord.Interaction, height: int) -> None:
    await interaction.response.send_message(await focus.set_height(height))

# focus set steps
@client.tree.command(name="sd_steps", description="Set the number of steps.")
async def set_steps(interaction: discord.Interaction, steps: int) -> None:
    await interaction.response.send_message(await focus.set_steps(steps))

# focus set cfg scale
@client.tree.command(name="sd_cfg_scale", description="Set the cfg scale.")
async def set_cfg_scale(interaction: discord.Interaction, cfg_scale: float) -> None:
    await interaction.response.send_message(await focus.set_cfg_scale(cfg_scale))

# focus set batch count
@client.tree.command(name="sd_batch_count", description="Set the batch count.")
async def set_batch_count(interaction: discord.Interaction, batch_count: int) -> None:
    await interaction.response.send_message(await focus.set_batch_count(batch_count))

# focus set batch size
@client.tree.command(name="sd_batch_size", description="Set the batch size.")
async def set_batch_size(interaction: discord.Interaction, batch_size: int) -> None:
    await interaction.response.send_message(await focus.set_batch_size(batch_size))

# focus list models
@client.tree.command(name="sd_list_models", description="List available models.")
async def list_models(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(await focus.list_models())
## Ollama ##
# ollama list
@client.tree.command(name="ollama_list", description="List available models.")
async def ollama_list(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(await ollama.list())

# ollama run
@client.tree.command(name="ollama_run", description="Set the ollama model to use.")
async def ollama_run(interaction: discord.Interaction, model: str) -> None:
    await interaction.response.send_message(await ollama.set_model(model))

# ollama pull
@client.tree.command(name="ollama_pull", description="Pull a model.")
async def ollama_pull(interaction: discord.Interaction, model: str) -> None:
    await interaction.response.send_message(await ollama.pull(model))

# ollama rm
@client.tree.command(name="ollama_rm", description="Remove a model.")
async def ollama_rm(interaction: discord.Interaction, model: str) -> None:
    await interaction.response.send_message(await ollama.rm(model))


## GPT ##
# gpt list
@client.tree.command(name="gpt_list", description="List available models.")
async def gpt_list(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(await gpt.list())

# gpt run
@client.tree.command(name="gpt_run", description="Set the gpt model to use.")
async def gpt_run(interaction: discord.Interaction, model: str) -> None:
    await interaction.response.send_message(await gpt.set_model(model))

# clear chat history
@client.tree.command(name="clear_chat_history", description="Clear the chat history.")
async def clear_chat_history(interaction: discord.Interaction) -> None:
    conversation_history[interaction.channel.id] = []
    await interaction.response.send_message("Chat history cleared.")



@client.event
async def on_ready():
    await client.tree.sync()
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Initialize conversation history for the channel if it doesn't exist
    if message.channel.id not in conversation_history:
        conversation_history[message.channel.id] = []

    # Append the user's message to the conversation history
    conversation_history[message.channel.id].append({"role": "user", "content": message.content})
    if LM_PROVIDER == 'ollama':
        # Send chat request to Ollama
        response = await ollama.chat(conversation_history[message.channel.id])
    elif LM_PROVIDER == 'gpt':
        # Send chat request to GPT
        response = await gpt.chat(conversation_history[message.channel.id])
    # Append the model's response to the conversation history
    conversation_history[message.channel.id].append({"role": "assistant", "content": response})
    # Split the response if it exceeds Discord's character limit
    for chunk in await utlis.format_response(response):
        await message.channel.send(chunk)

client.run(TOKEN)