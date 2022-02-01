import random
import discord
from discord.ext import commands
from cogs.wallet import walletUtils

class rewards(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def onMessageListener(self, message):
        playerData = walletUtils.loadJson()
        if str(message.author.id) in list(playerData.keys()):
            i = random.randrange(1,6)
            if i == 1:
                playerData[str(message.author.id)]["balance"] += 1
                walletUtils.saveJson(playerData)


    @commands.Cog.listener("on_reaction_add")
    async def onReactListener(self,reaction,user):
        playerData = walletUtils.loadJson()
        if str(user.id) in list(playerData.keys()):
            i = random.randrange(1,4)
            if i == 1:
                
                playerData[str(user.id)]["balance"] += 1
                walletUtils.saveJson(playerData)
        else:
            pass


def setup(bot):
        bot.add_cog(rewards(bot))