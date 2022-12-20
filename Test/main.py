import discord

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Bot is ready!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await message.channel.send("Hello!")
        
TOKEN = "MTA1NDA5ODYyNjgxNDY3NzE3Mg.G99wQG.ZRz2vmliuzn0OwuniPGlNjYhPcLo9lmVLo5HAw"
client.run(TOKEN)