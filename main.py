import discord
from discord.ext import commands
from config import *
import focus
# import ollama
import litellm
# import gpt
# import claude
import utlis

# Create a new client instance
intents = discord.Intents.all()
client = commands.Bot(command_prefix="/", intents=intents)
tree = client.tree

# Dictionary to store conversation history for each channel
conversation_history = {}
# @client.tree.command(name="use_litellm", description="Set LM provider to LiteLLM.")
# async def use_litellm(interaction: discord.Interaction) -> None:
#     global LM_PROVIDER
#     LM_PROVIDER = "litellm"
#     await interaction.response.send_message("LM provider set to LiteLLM.")

# liteellm list
@client.tree.command(name="list", description="List available models.")
async def ollama_list(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(await litellm.list_models())

# liteellm run
@client.tree.command(name="run", description="Set the LiteLLM model to use.")
async def litellm_run(interaction: discord.Interaction, model: str) -> None:
    await interaction.response.send_message(await litellm.set_model(model))

# new chat
# create a new text channel in chats category
@client.tree.command(name="new_chat", description="Create a new chat.")
async def new_chat(interaction: discord.Interaction) -> None:
    await interaction.response.send_message("Creating a new chat...")
    
    # Find the "chats" category by name
    chats_category = None
    for category in interaction.guild.categories:
        if category.name.lower() == "chats":
            chats_category = category
            break
    
    # If "chats" category doesn't exist, create it
    if chats_category is None:
        chats_category = await interaction.guild.create_category("chats")
        await interaction.followup.send("Created 'chats' category since it didn't exist.")
    
    # Create a new text channel in the chats category
    import datetime
    timestamp = datetime.datetime.now().strftime("%m-%d-%H%M")
    channel_name = f"chat-{timestamp}"
    
    channel = await interaction.guild.create_text_channel(
        name=channel_name, 
        category=chats_category
    )
    await interaction.followup.send(f"Chat created: {channel.mention}")


# @client.tree.command(name="use_ollama", description="Set LM provider to Ollama.")
# async def use_ollama(interaction: discord.Interaction) -> None:
#     global LM_PROVIDER
#     LM_PROVIDER = "ollama"
#     await interaction.response.send_message("LM provider set to Ollama.")

# @client.tree.command(name="use_gpt", description="Set LM provider to GPT.")
# async def use_gpt(interaction: discord.Interaction) -> None:
#     global LM_PROVIDER
#     LM_PROVIDER = "gpt"
#     await interaction.response.send_message("LM provider set to GPT.")

# @client.tree.command(name="use_claude", description="Set LM provider to Claude.")
# async def use_claude(interaction: discord.Interaction) -> None:
#     global LM_PROVIDER
#     LM_PROVIDER = "claude"
#     await interaction.response.send_message("LM provider set to Claude.")


## Focus ##
# focus txt2img
@client.tree.command(name="sd", description="Generate an image from a prompt.")
async def sd(interaction: discord.Interaction, prompt: str) -> None:
    await interaction.response.defer(thinking=True)
    await utlis.generate_and_send_images(interaction, prompt)

# focus set model
@client.tree.command(name="sd_model", description="Set the model to use.")
async def sd_model(interaction: discord.Interaction, model: str) -> None:
    await interaction.response.send_message(await focus.set_model(model))

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


# ## Ollama ##
# # ollama list
# @client.tree.command(name="ollama_list", description="List available models.")
# async def ollama_list(interaction: discord.Interaction) -> None:
#     await interaction.response.send_message(await ollama.list())

# # ollama run
# @client.tree.command(name="ollama_run", description="Set the ollama model to use.")
# async def ollama_run(interaction: discord.Interaction, model: str) -> None:
#     await interaction.response.send_message(await ollama.set_model(model))

# # ollama pull
# @client.tree.command(name="ollama_pull", description="Pull a model.")
# async def ollama_pull(interaction: discord.Interaction, model: str) -> None:
#     await interaction.response.send_message(await ollama.pull(model))

# # ollama rm
# @client.tree.command(name="ollama_rm", description="Remove a model.")
# async def ollama_rm(interaction: discord.Interaction, model: str) -> None:
#     await interaction.response.send_message(await ollama.rm(model))


# ## GPT ##
# # gpt list
# @client.tree.command(name="gpt_list", description="List available models.")
# async def gpt_list(interaction: discord.Interaction) -> None:
#     await interaction.response.send_message(await gpt.list())

# # gpt run
# @client.tree.command(name="gpt_run", description="Set the gpt model to use.")
# async def gpt_run(interaction: discord.Interaction, model: str) -> None:
#     await interaction.response.send_message(await gpt.set_model(model))




# clear chat history for current channel
@client.tree.command(name="clear_chat_history", description="Clear the chat history for this channel.")
async def clear_chat_history(interaction: discord.Interaction) -> None:
    if interaction.channel.id in conversation_history:
        conversation_history[interaction.channel.id] = []
        await interaction.response.send_message("✅ Chat history cleared for this channel.")
    else:
        await interaction.response.send_message("ℹ️ No chat history found for this channel.")

# view chat stats
@client.tree.command(name="chat_stats", description="View chat statistics and active conversations.")
async def chat_stats(interaction: discord.Interaction) -> None:
    embed = discord.Embed(title="📊 Chat Statistics", color=0x00ff00)
    
    # Count active conversations
    active_chats = len(conversation_history)
    embed.add_field(name="Active Conversations", value=f"{active_chats} channels", inline=True)
    
    # Find chats category channels
    chats_category = None
    for category in interaction.guild.categories:
        if category.name.lower() == "chats":
            chats_category = category
            break
    
    if chats_category:
        chat_channels = len(chats_category.channels)
        embed.add_field(name="Chat Channels", value=f"{chat_channels} in 'chats' category", inline=True)
        
        # List active conversations in chats category
        active_in_chats = []
        for channel in chats_category.channels:
            if channel.id in conversation_history and conversation_history[channel.id]:
                message_count = len(conversation_history[channel.id])
                active_in_chats.append(f"• {channel.mention} ({message_count} messages)")
        
        if active_in_chats:
            embed.add_field(name="Active Chats", value="\n".join(active_in_chats[:10]), inline=False)
            if len(active_in_chats) > 10:
                embed.add_field(name="", value=f"... and {len(active_in_chats) - 10} more", inline=False)
        else:
            embed.add_field(name="Active Chats", value="No active conversations in chats category", inline=False)
    else:
        embed.add_field(name="Chat Channels", value="No 'chats' category found", inline=True)
    
    embed.add_field(name="Current Channel", 
                   value=f"{'✅ In chats category' if interaction.channel.category and interaction.channel.category.name.lower() == 'chats' else '❌ Not in chats category'}", 
                   inline=False)
    
    await interaction.response.send_message(embed=embed)

# delete current chat channel (only works in chats category)
@client.tree.command(name="delete", description="Delete this chat channel (only works in chats category).")
async def delete_chat(interaction: discord.Interaction) -> None:
    # Check if we're in a guild (not DM)
    if not interaction.guild:
        await interaction.response.send_message("❌ This command can only be used in a server.", ephemeral=True)
        return
    
    # Check if the channel is in the "chats" category
    if not interaction.channel.category or interaction.channel.category.name.lower() != "chats":
        await interaction.response.send_message("❌ This command only works in channels within the 'chats' category.", ephemeral=True)
        return
    
    # Check if user has manage channels permission or is admin
    if not (interaction.user.guild_permissions.manage_channels or interaction.user.guild_permissions.administrator):
        await interaction.response.send_message("❌ You need 'Manage Channels' permission to delete chat channels.", ephemeral=True)
        return
    
    channel_name = interaction.channel.name
    channel_id = interaction.channel.id
    
    # Clean up conversation history
    if channel_id in conversation_history:
        del conversation_history[channel_id]
    
    # Confirm deletion
    await interaction.response.send_message(f"🗑️ Deleting chat channel `{channel_name}` in 3 seconds...")
    
    # Wait a moment then delete the channel
    import asyncio
    await asyncio.sleep(3)
    
    try:
        await interaction.channel.delete(reason=f"Chat deleted by {interaction.user}")
    except Exception as e:
        # If we can't delete, try to send an error (though channel might already be gone)
        try:
            await interaction.followup.send(f"❌ Failed to delete channel: {str(e)}")
        except:
            print(f"Failed to delete channel {channel_name}: {e}")

# delete all chat channels at once (admin only)
@client.tree.command(name="delete_chats", description="Delete ALL chat channels at once (Admin only).")
async def delete_all_chats(interaction: discord.Interaction) -> None:
    # Check if we're in a guild (not DM)
    if not interaction.guild:
        await interaction.response.send_message("❌ This command can only be used in a server.", ephemeral=True)
        return
    
    # Check if user is administrator
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ This command requires Administrator permissions.", ephemeral=True)
        return
    
    # Find the "chats" category
    chats_category = None
    for category in interaction.guild.categories:
        if category.name.lower() == "chats":
            chats_category = category
            break
    
    if not chats_category:
        await interaction.response.send_message("❌ No 'chats' category found.", ephemeral=True)
        return
    
    # Get all text channels in the chats category
    chat_channels = [channel for channel in chats_category.channels if isinstance(channel, discord.TextChannel)]
    
    if not chat_channels:
        await interaction.response.send_message("ℹ️ No chat channels found to delete.", ephemeral=True)
        return
    
    channel_count = len(chat_channels)
    await interaction.response.send_message(f"🗑️ Deleting {channel_count} chat channels...")
    
    deleted_count = 0
    failed_deletions = []
    
    # Clear conversation histories first
    for channel in chat_channels:
        if channel.id in conversation_history:
            del conversation_history[channel.id]
    
    # Delete all channels
    import asyncio
    for channel in chat_channels:
        try:
            await channel.delete(reason=f"Bulk chat deletion by {interaction.user}")
            deleted_count += 1
            await asyncio.sleep(0.5)  # Small delay to avoid rate limits
        except Exception as e:
            failed_deletions.append(f"{channel.name}: {str(e)}")
    
    # Send results
    result_embed = discord.Embed(
        title="✅ Bulk Deletion Complete",
        color=0x00ff00
    )
    result_embed.add_field(name="Deleted", value=f"{deleted_count} channels", inline=True)
    result_embed.add_field(name="Failed", value=f"{len(failed_deletions)} channels", inline=True)
    
    if failed_deletions:
        failures_text = "\n".join(failed_deletions[:5])
        if len(failed_deletions) > 5:
            failures_text += f"\n... and {len(failed_deletions) - 5} more"
        result_embed.add_field(name="Failures", value=failures_text, inline=False)
    
    await interaction.followup.send(embed=result_embed)

# clear channel by deleting and recreating it
@client.tree.command(name="clear", description="Clear this channel by deleting and recreating it.")
async def clear_channel(interaction: discord.Interaction) -> None:
    # Check if we're in a guild (not DM)
    if not interaction.guild:
        await interaction.response.send_message("❌ This command can only be used in a server.", ephemeral=True)
        return
    
    # Check if user has manage channels permission or is admin
    if not (interaction.user.guild_permissions.manage_channels or interaction.user.guild_permissions.administrator):
        await interaction.response.send_message("❌ You need 'Manage Channels' permission to clear channels.", ephemeral=True)
        return
    
    # Store channel information before deletion
    old_channel = interaction.channel
    channel_name = old_channel.name
    channel_category = old_channel.category
    channel_position = old_channel.position
    channel_topic = old_channel.topic
    channel_slowmode = old_channel.slowmode_delay
    channel_nsfw = old_channel.nsfw
    
    # Store channel permissions
    channel_overwrites = old_channel.overwrites
    
    # Clear conversation history for this channel
    if old_channel.id in conversation_history:
        del conversation_history[old_channel.id]
    
    # Respond to the interaction
    await interaction.response.send_message(f"🔄 Clearing channel `{channel_name}` by recreating it...")
    
    try:
        # Create the new channel with the same properties
        new_channel = await interaction.guild.create_text_channel(
            name=channel_name,
            category=channel_category,
            topic=channel_topic,
            slowmode_delay=channel_slowmode,
            nsfw=channel_nsfw,
            overwrites=channel_overwrites,
            position=channel_position,
            reason=f"Channel cleared by {interaction.user}"
        )
        
        # Send confirmation message in the new channel
        await new_channel.send(f"✅ Channel cleared and recreated by {interaction.user.mention}")
        
        # Delete the old channel
        await old_channel.delete(reason=f"Channel cleared by {interaction.user}")
        
    except Exception as e:
        # If recreation fails, try to send error in the original channel
        try:
            await interaction.followup.send(f"❌ Failed to recreate channel: {str(e)}")
        except:
            print(f"Failed to clear channel {channel_name}: {e}")

# debug command to check bot permissions and status
@client.tree.command(name="debug", description="Check bot permissions and command sync status.")
async def debug(interaction: discord.Interaction) -> None:
    guild = interaction.guild
    bot_member = guild.get_member(client.user.id)
    
    embed = discord.Embed(title="Bot Debug Information", color=0x00ff00)
    
    # Check basic info
    embed.add_field(name="Bot User", value=f"{client.user} (ID: {client.user.id})", inline=False)
    embed.add_field(name="Guild", value=f"{guild.name} (ID: {guild.id})", inline=False)
    
    # Check permissions
    permissions = bot_member.guild_permissions
    important_perms = {
        "Use Slash Commands": permissions.use_slash_commands,
        "Send Messages": permissions.send_messages,
        "Read Messages": permissions.read_messages,
        "Embed Links": permissions.embed_links,
        "Attach Files": permissions.attach_files
    }
    
    perms_text = "\n".join([f"{'✅' if perm else '❌'} {name}" for name, perm in important_perms.items()])
    embed.add_field(name="Key Permissions", value=perms_text, inline=False)
    
    # Check if bot can see slash commands in this guild
    try:
        commands = await client.tree.fetch_commands(guild=guild)
        embed.add_field(name="Commands in Guild", value=f"Found {len(commands)} commands", inline=False)
    except:
        embed.add_field(name="Commands in Guild", value="❌ Error fetching commands", inline=False)
    
    await interaction.response.send_message(embed=embed)

# force sync commands to current guild (for testing)
@client.tree.command(name="force_sync", description="Force sync commands to this guild (Admin only).")
async def force_sync(interaction: discord.Interaction) -> None:
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ You need Administrator permissions to use this command.", ephemeral=True)
        return
    
    await interaction.response.defer()
    
    try:
        # Sync to current guild
        guild = discord.Object(id=interaction.guild.id)
        client.tree.copy_global_to(guild=guild)
        synced = await client.tree.sync(guild=guild)
        await interaction.followup.send(f"✅ Successfully synced {len(synced)} commands to this guild!")
    except Exception as e:
        await interaction.followup.send(f"❌ Error syncing commands: {str(e)}")



@client.event
async def on_ready():
    # Sync commands globally (takes up to 1 hour to propagate)
    await client.tree.sync()
    print(f'We have logged in as {client.user}')
    print("Commands synced globally")
    
    # Optional: Sync to a specific guild for instant testing (replace GUILD_ID)
    # Uncomment and replace YOUR_GUILD_ID_HERE with your server's ID for instant command sync
    # guild = discord.Object(id=YOUR_GUILD_ID_HERE)
    # client.tree.copy_global_to(guild=guild)
    # await client.tree.sync(guild=guild)
    # print(f"Commands synced to guild {YOUR_GUILD_ID_HERE}")
    
    # Alternative: Auto-sync to all guilds the bot is in (for development)
    for guild in client.guilds:
        try:
            client.tree.copy_global_to(guild=guild)
            await client.tree.sync(guild=guild)
            print(f"Commands synced to guild: {guild.name} ({guild.id})")
        except Exception as e:
            print(f"Failed to sync to {guild.name}: {e}")

async def shutdown():
    """Cleanup when bot shuts down."""
    print("Bot shutting down, cleaning up...")
    await litellm.cleanup_session()

@client.event
async def on_disconnect():
    await shutdown()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Only respond to messages in channels within the "chats" category
    if not message.guild:  # Skip DMs
        return
    
    # Check if the message is in a channel within the "chats" category
    if not message.channel.category or message.channel.category.name.lower() != "chats":
        return

    # Initialize conversation history for the channel if it doesn't exist
    if message.channel.id not in conversation_history:
        conversation_history[message.channel.id] = []

    # Append the user's message to the conversation history
    conversation_history[message.channel.id].append({"role": "user", "content": message.content})
    
    # Show typing indicator while processing
    try:
        async with message.channel.typing():
            if LM_PROVIDER == 'litellm':
                # Send chat request to LiteLLM
                response = await litellm.chat(conversation_history[message.channel.id])
            # elif LM_PROVIDER == 'ollama':
            #     # Send chat request to Ollama
            #     response = await ollama.chat(conversation_history[message.channel.id])
            # elif LM_PROVIDER == 'gpt':
            #     # Send chat request to GPT
            #     response = await gpt.chat(conversation_history[message.channel.id])
            # elif LM_PROVIDER == 'claude':
            #     # Send chat request to Claude
            #     response = await claude.chat(conversation_history[message.channel.id])
            else:
                response = "Error: No valid LM provider configured."
            
            # Append the model's response to the conversation history
            conversation_history[message.channel.id].append({"role": "assistant", "content": response})
            
            # Split the response if it exceeds Discord's character limit
            for chunk in utlis.format_response(response):
                await message.channel.send(chunk)
                
    except Exception as e:
        error_msg = f"Sorry, I encountered an error: {str(e)}"
        print(f"Error in on_message: {e}")
        
        # Try to send error message to user
        try:
            await message.channel.send(error_msg)
        except:
            print(f"Failed to send error message to channel {message.channel.id}")
            
        # Remove the user's message from history if we failed to process it
        if (message.channel.id in conversation_history and 
            conversation_history[message.channel.id] and 
            conversation_history[message.channel.id][-1]["role"] == "user"):
            conversation_history[message.channel.id].pop()

client.run(TOKEN)