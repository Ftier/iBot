#TODO:  
    #Add check to load/unload/reload
    #move api keys to gitignore
    #Votekick/mod commands cog
    #twitch plays pokemon style democracy vs anarchy but for mod commands
    #add pump and dump scheme /s
    #add prefix to config.json
 
import discord
import os
import json
from discord.ext import commands

with open("config.json","r") as f:
    jString = f.read()
    data = json.loads(jString)
    api_key = data["discordKey"]
    prefix = data["prefix"]
    f.close()


bot = commands.Bot(command_prefix=".")

intents = discord.Intents.default()
intents.members = True


#TODO: put role name in config.json (edit json from within discord perhaps?)
def hasRole(ctx: commands.Context, minRole:str = "Bot Daddy"):
    roles = [i for i in ctx.author.roles]
    roleNames = [j.name for j in roles]
    if minRole in roleNames:
        return True
    else:
        return False




@bot.event
async def on_ready():
    print("Bot is ready.")

#ping
@bot.command()
async def ping(ctx):
    """Returns the latency of the iBot - usage: ping"""
    await ctx.send(str("pong! with {0}".format(round(bot.latency,2)))+"ms")

#load
@bot.command()
async def load(ctx, extension):
    """Loads given extension - usage: load <extension name>"""
    if hasRole(ctx):
        try:
            bot.load_extension(f'cogs.{extension}')
        except Exception as e:
            await ctx.send(f"an error occured loading the {extension} extension")
            print(f"an error has occured loading extension {extension}  {e}")
    else:
        await ctx.send("You don't have permission to use that command. :(")

#unload
@bot.command()
async def unload(ctx, extension):
    """Unloads given extension - usage: unload <extension name>"""
    if hasRole(ctx):
        bot.unload_extension(f'cogs.{extension}')
    else:
        await ctx.send("You don't have permission to use that command. :(")

#reload
@bot.command()
async def reload(ctx, extension):
    if hasRole(ctx):
        try:
            bot.unload_extension(f'cogs.{extension}')
            bot.load_extension(f'cogs.{extension}')
            await ctx.send(f"The extension {extension} has been reloaded")
        except Exception as e:
            await ctx.send(f"An error occured loading {extension}. {e}")
    else:
        await ctx.send("You don't have permission to use that command. :(")
    
"""
for file in os.listdir(f'./cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')
"""

bot.run(api_key)

