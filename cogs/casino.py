import random
import discord
from discord.ext import commands
from cogs.wallet import walletUtils

class casino(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot

    #commands go here
    @commands.command()
    async def coinToss(self,ctx,amount:int):
        playerData = walletUtils.loadJson()
        playerId = str(ctx.author.id)
        if playerData[playerId]["balance"] >= amount:
            ht = random.randrange(2)
            if ht == 1:
                playerData[playerId]["balance"] = playerData[playerId]["balance"] + amount
                walletUtils.saveJson(playerData)
                await ctx.send(f"Congratulations, you won {amount} kwiffs")

            else:
                #Thanks for your donation
                playerData[playerId]["balance"] = playerData[playerId]["balance"] - amount
                walletUtils.saveJson(playerData)
                await ctx.send("Fat L. Do something about it.")
    
def setup(bot):
        bot.add_cog(casino(bot))