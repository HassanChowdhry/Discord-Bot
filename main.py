import discord
from discord.ext import commands
from os import getenv
from service.leetStats import getLeetStats, compareUsers
from dotenv import load_dotenv

# gets env var
load_dotenv()

# initialsinf bots - switch intents to default and message content to true bfr finish
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all(), case_insensitive=True)

# event when bot starts
@bot.event
async def on_ready():
    print("Bot is ready!")

# bot command - only accepts messages from specific server
@bot.command()
async def leet(ctx):
    if ctx.channel.name != "testing":
        return
    
    try:
        # reply for stats and send back as an embedded message
        embed = discord.Embed(title="", color=discord.Color.yellow())
        embed.title = "Enter your username"
        await ctx.send(embed=embed)
        
        # wait for user input
        username = await bot.wait_for("message", check=lambda m: m.author == ctx.author, timeout=60.0)
        username = username.content
        
        df = await getLeetStats(username=username)
        
        if df is not None:
            # Convert the DataFrame to a string for sending through Discord
            stats_message = df.to_string(index=False)
            
            # send as code block
            await ctx.send(f"```{stats_message}```")
        else:
            # username not found
            error_embed = discord.Embed(title="Error", description=f"Could not find leetcode account with the username {username}", color=discord.Color.red())
            await ctx.send(embed=error_embed)
    except commands.errors.CommandError as ce:
        print(f"CommandError: {ce}")
        error_embed = discord.Embed(title="Command Error", description="An error occurred during command execution.", color=discord.Color.red())
        await ctx.send(embed=error_embed)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        error_embed = discord.Embed(title="Unexpected Error", description="An unexpected error occurred.", color=discord.Color.red())
        await ctx.send(embed=error_embed)

@bot.command()
async def comparestats(ctx):
    if ctx.channel.name != "testing":
        return
    try:
        # first username
        embed = discord.Embed(title="", color=discord.Color.yellow())
        embed.title = "Enter the first username"
        await ctx.send(embed=embed)
        # wait for user input
        username1 = await bot.wait_for("message", check=lambda m: m.author == ctx.author, timeout=60.0)
        username1 = username1.content

        # second username
        embed.title = "Enter the second username"
        await ctx.send(embed=embed)
        # wait for user input
        username2 = await bot.wait_for("message", check=lambda m: m.author == ctx.author, timeout=60.0)
        username2 = username2.content
        
        df_comparison = await compareUsers(username1, username2)
    
        if df_comparison is not None:
            comparison_message = df_comparison.to_string(index=False)
            
            await ctx.send(f"```{comparison_message}```")
        else:
            # Error occurred during comparison
            error_embed = discord.Embed(title="Error", description="Could not find leetcode account with the username", color=discord.Color.red())
            await ctx.send(embed=error_embed)
    except commands.errors.CommandError as ce:
        print(f"CommandError: {ce}")
        error_embed = discord.Embed(title="Command Error", description="An error occurred during command execution.", color=discord.Color.red())
        await ctx.send(embed=error_embed)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        error_embed = discord.Embed(title="Unexpected Error", description="An unexpected error occurred.", color=discord.Color.red())
        await ctx.send(embed=error_embed)

# Handle wrong command
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        error_embed = discord.Embed(title="Command Not Found", description="The command you entered does not exist.", color=discord.Color.red())
        await ctx.send(embed=error_embed)

# lists all available commands (maybe help does same?)
@bot.command()
async def listcommands(ctx):
    command_list = [command.name for command in bot.commands]
    command_list.sort()
    commands_str = "\n".join(command_list)
    
    embed = discord.Embed(title="Available Commands", description=f"```\n{commands_str}\n```", color=discord.Color.green())
    await ctx.send(embed=embed)

TOKEN = getenv("TOKEN")
bot.run(TOKEN)