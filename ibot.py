import discord
import re
import emoji
import requests
from discord.ext import commands
from mcstatus import MinecraftServer

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', help_command=None)

#Global vars:
cmdlist = ['ss','poll']

@bot.event
async def on_ready():
    print("bot is ready")

@bot.command()
async def ss(ctx):
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


@bot.command()
async def poll(ctx):
    str = ""
    str = ctx.message.content
    pattern = '"(.*?)"'

    question = re.search(pattern, str).group(1)
    #print(question)

    options = str[8+len(question):].rstrip().split(',')
    #print(options)

    num2emote = {0:':zero:', 1: ':one:', 2: ':two:', 3: ':three:', 4: ':four:',
        5: ':five:', 6: ':six:', 7: ':seven:', 8: ':eight:', 9: ':nine:'}
    
    output = question + '\n'
    j=0
    for i in options:
        if i[0] == " ":
            i = i[1:]
        j += 1
        output = output + num2emote[j] + ' - ' + i + '\n'
    #print(output)
    msg = await ctx.channel.send(output)
    for i in range(j):
        await msg.add_reaction(emoji.emojize(num2emote[i+1],use_aliases=True))

@bot.command()
async def strawpoll(ctx):
    #string = input("\nType Command: ")
    string = ctx.message.content
    pattern = '"(.*?)"'

    question = re.search(pattern, string).group(1)
    #print(question)

    options = string[len('!strawpoll ""')+len(question):].split(',')
    j=0
    for i in options:
        if i[0] == " ":
            options[j] = i[1:]
        j+=1
    #print(options)



    api_key = 'P1PDKGJC2D91GRP1AZYC9WKPY36ORKJ2';

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

    poll = requests.post("https://strawpoll.com/api/poll", json=data, headers={'API-KEY': api_key}).json()

    print(poll)
    print(poll["content_id"])

    embedLink = "https://strawpoll.com/embed/" + poll["content_id"]
    urlVar = "https://strawpoll.com/" + poll["content_id"]
    #titleVar = '<iframe width="620" height="572" src=' + embedLink +' style="width: 100%; height: 572px;" frameborder="0" allowfullscreen></iframe>'
    optionsVar = ""
    for i in options:
        optionsVar = optionsVar + '- ' + i + '\n'
    
    embedVar = discord.Embed(title=question,url = urlVar, description="", color=0x00ffff)
    embedVar.add_field(name="Options:", value = optionsVar, inline = False)
    await ctx.channel.send(embed=embedVar)

@bot.command()
async def help(ctx):
    if len(ctx.message.content) > len('!help '):
        cmd = ctx.message.content[6:]
        print(cmd)
        if cmd not in cmdlist:
            await ctx.channel.send("That doesn't appear to be a valid command. use !help to see available commands.")      
        elif cmd == 'ss':
            await ctx.channel.send('Server Status - usage: !ss - gives the current status of the CobC minecraft server')
        elif cmd == 'poll':
            await ctx.channel.send('Poll - usage: !poll "Question (include quotation marks)" option 1, option 2, option 3 - Creates a reaction poll with options seperated by commas.')
        elif cmd == 'strawpoll':
            await ctx.channel.send('Strawpoll - usage: !strawpoll "Question (include quotation marks)" option 1, option 2, option 3 - Creates a strawpoll with options seperated by commas.')
        
    elif len(ctx.message.content) == len('!help'):
        await ctx.channel.send("""Here are a list of available currently available commands:     
        !ss - usage: !ss - gives the current status of the CobC minecraft server 
        !poll - usage: !poll "Question between quotes" option1 option2 option3 - creates a poll and buttons to vote with
        !strawpoll - usage: !strawpoll "Question (include quotation marks)" option 1, option 2, option 3 - Creates a strawpoll with options seperated by commas.""")


bot.run('ODY3MjQ4MTg4MjI2MDExMTU2.YPeV0A.67KjugPm9OqfnCs-JXFKlJ4xwng')


