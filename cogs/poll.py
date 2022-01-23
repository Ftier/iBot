#TODO
#implement hidden api keys

import discord
import emoji
import re
import requests
from discord.ext import commands



class poll(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot

    #commands go here:
    @commands.command()
    async def poll(self,ctx):
        '''Create a quick poll, using reactions to cast votes. This poll is **NOT anonymous**. - usage: poll <"Insert question between quotes"> option 1, option 2, option 3'''

        #define dictionary to help handle emojis
        num2emote = {0:':zero:', 1: ':one:', 2: ':two:', 3: ':three:', 4: ':four:', 5: ':five:', 6: ':six:', 7: ':seven:', 8: ':eight:', 9: ':nine:'}

        #extract contents of command
        msg = str(ctx.message.content)
        pattern = '"(.*?)"'

        #seperate question and options from msg
        question = re.search(pattern, msg).group(1)
        options = msg[8+len(question):].rstrip().split(',')

        #create output string        
        output = question + '\n'
        j=0
        for i in options:
            if i[0] == " ":
                i = i[1:]
            j += 1
            output = output + num2emote[j] + ' - ' + i + '\n'
        #print(output)

        #send output and add emojis to message
        msg = await ctx.channel.send(output)
        for i in range(j):
            await msg.add_reaction(emoji.emojize(num2emote[i+1],use_aliases=True))

    @commands.command()
    async def strawpoll(self,ctx):
        '''Creates a poll using strawpoll, lists the options and provides a hyperlink to the poll.'''
        #initialize vars
        string = ctx.message.content
        pattern = '"(.*?)"'

        #separate question and options
        question = re.search(pattern, string).group(1)
        options = string[len('!strawpoll ""')+len(question):].split(',')
        j=0
        for i in options:
            if i[0] == " ":
                options[j] = i[1:]
            j+=1

        api_key = 'P1PDKGJC2D91GRP1AZYC9WKPY36ORKJ2';

        #create data packet
        data = {
            "poll": {
                "title": question,
                "answers": options,
                # "description": "Description Text",
                # "priv": 1,
                # "ma": 0,
                # "mip": 0,
                # "co": 1,
                # "vpn": 0,
                # "enter_name": 0,
                # "has_deadline": 1,
                # "deadline": "2020-02-27T07:00:00.000Z",
                # "only_reg": 0,
                # "has_image": 0,
                # "image": None,
            }
        }


        #send data to strawpoll
        poll = requests.post("https://strawpoll.com/api/poll", json=data, headers={'API-KEY': api_key}).json()
        print(poll)
        print(poll["content_id"])

        #create then send embed
        embedLink = "https://strawpoll.com/embed/" + poll["content_id"]
        urlVar = "https://strawpoll.com/" + poll["content_id"]
        #titleVar = '<iframe width="620" height="572" src=' + embedLink +' style="width: 100%; height: 572px;" frameborder="0" allowfullscreen></iframe>'
        optionsVar = ""
        for i in options:
            optionsVar = optionsVar + '- ' + i + '\n'
        embedVar = discord.Embed(title=question,url = urlVar, description="", color=0x00ffff)
        embedVar.add_field(name="Options:", value = optionsVar, inline = False)
        await ctx.channel.send(embed=embedVar)


def setup(bot):
        bot.add_cog(poll(bot))