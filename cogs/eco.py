import discord
import json
from discord.ext import commands
from discord.utils import get

class eco(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    #commands
    @commands.command()
    async def wallet(self,ctx):
        """Check the balance of your wallet. - usage: wallet"""
        playerId = ctx.author.id


        f = open('cogs/data.json','r')        
        data = json.load(f)
        print('json loaded')
     
        if str(playerId) not in data.keys():
            f = open('cogs/data.json','w')   
            newWallet = {
                "playerId"  :   playerId,
                "balance"   :   0,
                "rich"      :   False
            }


            data[str(playerId)] = newWallet
            jstring = json.dumps(data)
            f.write(jstring)
            
            print(data)

            await ctx.author.send(f"New wallet created with a balance of 0. You can now use the pay and request commands")
            #potential follow up?
            print('new wallet added')

        else:
            bal = data[str(playerId)]["balance"]
            await ctx.author.send(f"Your current wallet balance is {bal} keflers")
            print(f'got the balance of an existing wallet. balance is {bal}')
        print(list(data.keys()))
        
    @commands.command()
    async def pay(self,ctx,player,qty: int):
        """Sends currency to another user. Make sure you @ the other user - usage: pay @player amount -Example: pay @ibot 69"""
#        print(player)
#        print(qty)
        senderId = ctx.author.id
        recipId = int(player[3:-1])

        f = open('cogs/data.json','r')
        data = json.load(f)

        try:
            senderBal = data[str(senderId)]["balance"]
            recipBal = data[str(recipId)]["balance"]
            
            if senderBal >= qty:
                data[str(senderId)]["balance"] = senderBal - qty
                data[str(recipId)]["balance"] = recipBal + qty

                jstring = json.dumps(data)
                f = open('cogs/data.json','w')
                f.write(jstring)

                await ctx.author.send("Sucessful Transfer!")
                #TODO: alert the recipient
            else:
                await ctx.author.send("You can't afford that.")

        except ValueError:
            await ctx.send("that player doesn't have a wallet. use the wallet command to create one.")
        except Exception as e:
            print(f'an error occured {e}')


def setup(bot):
            bot.add_cog(eco(bot))