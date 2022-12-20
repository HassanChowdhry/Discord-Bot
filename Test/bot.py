import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('MTA1NDA5ODYyNjgxNDY3NzE3Mg.G99wQG.ZRz2vmliuzn0OwuniPGlNjYhPcLo9lmVLo5HAw')
