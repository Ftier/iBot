import discord
from discord.ext import commands
from mcstatus import MinecraftServer

class mcserver(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    #comands:
    @commands.command()
    async def ss(self,ctx):
        """Server Status. Gives the current status of the CobC minecraft server - usage: ss"""
        server = MinecraftServer("144.202.84.103",25565)
        latency = server.status().latency
        whosOnline = list(server.query().players.names)
        
        if latency < 5000:
            await ctx.channel.send('The minecraft server is **online!** with **' + str(len(whosOnline)) + '** players.')# \nLatency = '+ str(latency) + 'ms')
            
            if len(whosOnline) > 0:
                await ctx.channel.send('Online players are: **' + ',  '.join(whosOnline[0:-1]) + ' **and** ' + str(whosOnline[-1])+'**')
            else:
                await ctx.channel.send('No players currently online :[')
            await ctx.channel.send('Message of the day: **' + server.query().motd + '**')
        else:
            await ctx.channel.send('The server seems to be offline :/')

def setup(bot):
        bot.add_cog(mcserver(bot))