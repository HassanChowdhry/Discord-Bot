import discord
from discord.ext import commands
from os import getenv
from service.leetStats import getLeetStats
from dotenv import load_dotenv

# gets env var
load_dotenv()

# initialsinf bots - switch intents to default and message content to true bfr finish
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), case_insensitive=True)

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
    msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author)
    if msg.content.lower() in "leetcode":
        embed.title = "Enter your username"
        await ctx.send(embed=embed)
        username = await bot.wait_for("message", check=lambda m: m.author == ctx.author)
        username = username.content
        df = await getLeetStats(username=username)
        
        # Convert the DataFrame to a string for sending through Discord
        stats_message = df.to_string(index=False)
        
        # Sending the stats as a code block for better formatting
        await ctx.send(f"```{stats_message}```")
    
    else:
        embed.title = "Not available"
        await ctx.send(embed=embed)

#     await bot.process_commands(message) # when overriding discords built in methods
    
TOKEN = getenv("TOKEN")
bot.run(TOKEN)