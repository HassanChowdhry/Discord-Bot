import discord
import os
from dotenv import load_dotenv

# gets env var
load_dotenv()

# intents - bs for disc to work
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# event when bot starts
@client.event
async def on_ready():
    print("Bot is ready!")

# command when there is a message in server
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await message.channel.send("Hello!")

# gets tokem
TOKEN = os.getenv("TOKEN")
client.run(TOKEN)