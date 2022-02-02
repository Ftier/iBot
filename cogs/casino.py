import random
import discord
from discord.ext import commands
from cogs.wallet import walletUtils

class lottery():
    active = False
    players = []
    pool = 0
    duration = 60.0

class casino(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot
        self.activeLottery = self.lottery(self.bot)

    #commands go here
    @commands.command(nam="cointoss", aliases=["ct"], usage="<amount>",help="Flip a coin, heads you win. Tails, you lose.")
    async def cointoss(self,ctx,bet:int):
        amount = bet*0.25
        playerData = walletUtils.loadJson()
        playerId = str(ctx.author.id)
        if playerData[playerId]["balance"] >= bet and bet > 0:
            ht = random.randrange(2)
            if ht == 1:
                playerData[playerId]["balance"] = playerData[playerId]["balance"] + amount
                walletUtils.saveJson(playerData)
                await ctx.send(f"Heads! Congratulations, you won {amount}")

            else:
                #Thanks for your donation
                playerData[playerId]["balance"] = playerData[playerId]["balance"] - bet
                walletUtils.saveJson(playerData)
                await ctx.send("Tails. Thats a fat L. Do something about it.")
  


    
def setup(bot):
        bot.add_cog(casino(bot))


