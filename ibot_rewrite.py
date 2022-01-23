import discord
import os
from discord.ext import commands


bot = commands.Bot(command_prefix=".")

@bot.event
async def on_ready():
    print("Bot is ready.")

#ping
@bot.command()
async def ping(ctx):
    """Returns the latency of the iBot - usage: ping"""
    await ctx.send(str("pong! {0}".format(round(bot.latency,2)))+"ms")

#load
@bot.command()
async def load(ctx, extension):
    """Loads given extension - usage: load <extension name>"""
    try:
        bot.load_extension(f'cogs.{extension}')
    except Exception as e:
        await(ctx.send(f"an error occured loading the {extension} extension"))
        print(f"an error has occured loading extension {extension}  {e}")

#unload
@bot.command()
async def unload(ctx, extension):
    """Unloads given extension - usage: unload <extension name>"""
    bot.unload_extension(f'cogs.{extension}')

#reload
@bot.command()
async def reload(ctx, extension):
    try:
        bot.unload_extension(f'cogs.{extension}')
        bot.load_extension(f'cogs.{extension}')
        await ctx.send(f"The extension {extension} has been reloaded")
    except Exception as e:
        await ctx.send(f"An error occured loading {extension}. {e}")

"""
for file in os.listdir(f'./cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')
"""

bot.run("ODUxMDU0OTE2MjY4ODUxMjEx.YLyspw.20JB9NjKFX1aOalxtRGcEfN0de8")