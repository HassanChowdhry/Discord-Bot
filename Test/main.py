import discord
from discord.ext import commands
from os import getenv

from dotenv import load_dotenv

# gets env var
load_dotenv()
# initialsinf bots - switch intents to default and message content to true bfr finish
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# event when bot starts
@bot.event
async def on_ready():
    print("Bot is ready!")

# bot command - only accepts messages from specific server
@bot.command()
async def stats(ctx):
    if ctx.channel.name != "testing":
        return
    
    #reply for stats and sends back as an embedded message
    quotedText = 'Which *stats* do you want?'
    embed=discord.Embed(title= quotedText, color=discord.Color.blue())
    await ctx.send(embed=embed)
    
    # for now sends back which applications stats we want
    msg = await bot.wait_for("message")
    if msg.content == "Leetcode":
        embed.title = "Enter your username"
        await ctx.send(embed=embed)
        username = await bot.wait_for("message")
        
    else:
        embed.title = "Not available"
        await ctx.send(embed=embed)

#     await bot.process_commands(message) # when overriding discords built in methods
    
TOKEN = getenv("TOKEN")
bot.run(TOKEN)