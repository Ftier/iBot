from argparse import ArgumentError
import discord
import json
import emoji
from discord.ext import commands
from discord.utils import get

class wallet(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    def newPlayer(name: str, playerId: int, balance: int = 100):
        newWallet = {
            "playerId"      :       playerId,
            "name"          :       name,
            "balance"       :       balance
        }
        playerData = walletUtils.loadJson()
        playerData[str(playerId)] = newWallet
        walletUtils.saveJson(playerData)
        return



    #TODO: Fix request subcommand (not detecting reactions on message)
    @commands.group(invoke_without_command=True)
    async def wallet(self,ctx: commands.Context):
        """[balance|send]. Use !help wallet [balance|send] to see usage."""
        try:
            playerData = walletUtils.loadJson()
            walletInData = bool(walletUtils.checkForWallet(ctx.author.id))
            if walletInData:
                await ctx.send("do !help wallet to see wallet commands")         
            else:
                wallet.newPlayer(ctx.author.name, int(ctx.author.id))
                await ctx.send("New wallet created! You can see other wallet commands by doing !help wallet")
        except ArgumentError:
            await ctx.send("Use !help wallet [balance|send] to see correct usage.\n(Make sure you @ the person you're trying to transfer)")


    @wallet.command(name="balance",
                    aliases=["bal"],
                    usage = "",
                    help =  "Show the balance of your wallet.") 
    async def balance(self,ctx):
        if walletUtils.checkForWallet(ctx.author.id):
            playerData = walletUtils.loadJson()
            playerId = str(ctx.author.id)
            bal = playerData[playerId]["balance"]
            await ctx.send(f"Your current wallet balance is {bal}.")
        else:
            await ctx.send("You don't have a wallet yet. Do !wallet to create one.")


    @wallet.command(name="send",
                    usage = "<name> <amount>",
                    help = "Send money to someone else. (Make sure to @ them)")
    async def send(self,ctx: commands.Context,target: discord.Member, amount: int):
        playerData = walletUtils.loadJson()
        playerId = str(ctx.author.id)
        targetId = str(target.id)

        if walletUtils.checkForWallet(target.id):


            if playerData[playerId]["balance"] < amount:
                await ctx.send("Insufficient funds.")
            else:
                playerData[playerId]["balance"] = playerData[playerId]["balance"] - amount
                playerData[targetId]["balance"] = playerData[targetId]["balance"] + amount
                walletUtils.saveJson(playerData)
                await ctx.send("Transfer Succesful.")
        else:
            await ctx.send("That user doesn't have a wallet yet.  Do !wallet to create one.")

"""
    @wallet.command(name="request", 
                    aliases=["rq"],
                    usage = "<recipient name> <amount>",
                    help="Request funds from another player")
    async def request(self,ctx,target: discord.Member,amount):
        playerName = ctx.author.name
        if walletUtils.checkForWallet(target.id):
            message = await target.send(f"{playerName} is requesting that you send them {amount} kwiff(s). You can agree to the transfer by reacting :white_check_mark: and decline by clicking :x:")
            await message.add_reaction(emoji.emojize(":white_check_mark:",use_aliases=True))
            await message.add_reaction(emoji.emojize(":x:",use_aliases=True))

#TODO: This next line isn't properly detecting reactions           
#            reaction, user = await self.bot.wait_for("reaction_add")
            if reaction.emoji == ":x:":
                await target.send("The transfer was declined.")
                await ctx.author.send("The transfer was declined")

            elif reaction.emoji == ":white_check_mark":
                playerData = walletUtils.loadJson()
                playerData[str(target.id)]["balance"] = playerData[str(target.id)]["balance"] - amount
                playerData[str(ctx.author.id)]["balance"] = playerData[str(ctx.author.id)]["balance"] + amount
                walletUtils.saveJson(playerData)
                await ctx.author.send("The transfer was succesful.")
                await target.send("The transfer was succesful.")

        else:
            await ctx.send("That player has not created a wallet yet. Create a new wallet by using the !wallet command")
"""



def setup(bot):
            bot.add_cog(wallet(bot))


class walletUtils:
    def loadJson():
        f = open("data.json", "r")
        jString = str(f.read())
        playerData = json.loads(jString)
        f.close()
        return playerData

    def saveJson(playerData: dict):
        jString = json.dumps(playerData)
        f = open("data.json", "w")
        f.write(jString)
        f.close()
    
    def checkForWallet(playerId:int):
        playerData = walletUtils.loadJson()
        keys = list(playerData.keys())
        if str(playerId) in keys:
            return True
        else:
            return False

