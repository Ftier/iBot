import math
import discord
from discord.ext import commands
from wallet import walletUtils

class casino(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot

    #commands go here
    @commands.command()
    async def coinToss(self,ctx,amount):
        playerData = 



def setup(bot):
    bot.add_cog(casino(bot))