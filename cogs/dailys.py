import schedule
import time
import discord
from discord.ext import commands
from cogs.wallet import walletUtils

class dailys(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    def resetWordleFlag():
        data = walletUtils.loadJson()
        for playerId in list(data.keys()):
            data[playerId]["wordleFlag"] = False
        walletUtils.saveJson(data)

    schedule.every().day.at("12:00").do(resetWordleFlag())

#    while True:
 #       schedule.run_pending()
  #      time.sleep(1)

def setup(bot):
        bot.add_cog(dailys(bot))