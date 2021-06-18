#bot.py
#-----------------------------------------
#Required Packages:
#pip install pynacl
#pip install -U discord.py
#pip install -U python-dotenv
#pip install -U youtube_dl
#pip install -U discord.py[voice]
#
#-----------------------------------------
import os
import asyncio

import discord
from dotenv import load_dotenv
from discord.ext import commands

import youtube_dl

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') 

bot = commands.Bot(command_prefix=',')



# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

players = {}

currentID = 0

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5, file_name=''):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')
        self.id = data.get('id')
        self.duration = data.get('duration')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        cls.file_name = ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)



@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    print(f'{bot.guilds}')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('in hell'))
    

@bot.command(name='ping')
async def ping(ctx):
    if (ctx.author == bot.user):
        return
    
    await ctx.send('Pong!')
    
@bot.command(name='connect')
async def voiceConnect(ctx):
    voice_client = ctx.author.voice
    if (voice_client is None):
        await ctx.send('You are not in a voice channel!')
    elif (ctx.guild.voice_client is not None):
        await ctx.send('I am already connected!')
        return
    else:
        await voice_client.channel.connect(timeout=30.0,reconnect=True)
        await ctx.send('Connected!')
        print(f'{ctx.author.voice.channel}')
        
@bot.command(name='disconnect')
async def voiceDisconnect(ctx):
    voice_client = ctx.author.guild.voice_client
    if (voice_client is not None):
        await voice_client.disconnect(force=False)
    print(f'{bot.voice_clients}')

@bot.command(name='bombito')
async def bombito(ctx):
    Embed = discord.Embed(title='Title', description='Description', colour=discord.Colour.red(), url='https://www.youtube.com/watch?v=yrQgCz_Hr2U')
    stringTest = 'Bombito'
    Embed.add_field(name='bruh', value='[%s](https://www.youtube.com/watch?v=yrQgCz_Hr2U) Im bad' % stringTest)
    await ctx.send(embed=Embed)

#    try:
#        await voiceConnect(ctx)
#    except discord.ClientException:
#        print('Already connected!')
#    if (ctx.author.voice is not None):
#        voice_client = ctx.author.guild.voice_client
#        if (not voice_client.is_playing()):
#            player = await YTDLSource.from_url('https://www.youtube.com/watch?v=yrQgCz_Hr2U')
#            voice_client.play(player)
#            players[ctx.author.guild.id] = player
#        else:
#            await ctx.send('Already playing!')
@bot.command(name='play')
async def play(ctx, *, url):
    if (ctx.author.voice is None):
        await ctx.send('You are not in a voice channel!')
        return
    elif ctx.guild.voice_client is None:
        await ctx.author.voice.channel.connect(timeout=30.0,reconnect=True)
    
    voice_client = ctx.guild.voice_client
    id = ctx.guild.id
    player = None
    player = await YTDLSource.from_url(url)
    #try:
        #player = await YTDLSource.from_url(url)
        #player = await YTDLSource.create_source(ctx, url, download=False)
    #except:
     #   await ctx.send('Invalid URL!')
      #  return
    
    Embed = discord.Embed(title=player.title, description='Requested by ' + ctx.author.name, colour=discord.Colour.red(), url='https://www.youtube.com/watch?v=' + player.id)
    Embed.set_author(name='Added to queue')
    await ctx.send(embed=Embed)
    #await ctx.send('Added *' + player.title +'* to the queue!')
    if (id not in players):
        players[id] = [(player, player.file_name, ctx.author)]
    else:
        players[id].append((player, player.file_name, ctx.author))
    
    if (not voice_client.is_playing()):
        voice_client.play(player, after=lambda x: my_after(ctx))
    
    
    
#    try:
#        validURL = True
#        guildQueue = players[ctx.author.guild.id]
#        player = None
#        try:
#            player = await YTDLSource.from_url(url)
#        except:
#            validURL = False
#        
#        if (validURL):
#            if (len(guildQueue) == 0):
#                players[ctx.author.guild.id].append(player)
#                if (not voice_client.is_playing()):
#                    voice_client.play(player, after=lambda x: my_after(ctx))
#                
#            else:
#                players[ctx.author.guild.id].append(player)
#        else:
#            await ctx.send('Invalid URL!')
#    except KeyError:
#        validURL = True
#        player = None
#        try:
#            player = await YTDLSource.from_url(url)
#        except:
#            validURL = False
#            
#        if (validURL):
#            players[ctx.author.guild.id] = [player]
#            voice_client.play(player, after=lambda x: my_after(ctx))
#        else:
#            await ctx.send('Invalid URL!')
    
            
#TODO: Add checking for items in queue with same value
def my_after(ctx):
    guildID = ctx.author.guild.id
    playersList = players[guildID][0][1]
    #playersList[0].cleanup()
    for i in range(len(players[guildID])):
        print(players[guildID][i][1])
    players[guildID].pop(0)
    foundFile = False
    print("TEST")
    for i in players[guildID]:    
        print(i[1])
        if (playersList == i[1]):
            foundFile = True
            break
    print (foundFile)
    if (foundFile == False):
        try:
            os.remove(playersList)
        except:
            print("Wasn't able to find file, file_name: " + playersList)
            return
    
    if (len(players[ctx.author.guild.id]) != 0):
        ctx.guild.voice_client.play(players[guildID][0][0], after=lambda x: my_after(ctx))
    else:
        #await ctx.send('Queue has been emptied')
        print('Queue has been emptied!')

@bot.command(name='queue')
async def queue(ctx):
    id = ctx.author.guild.id
    if (id not in players):
        await ctx.send('Nothing in the queue!')
    elif (players[id] == []):
        await ctx.send('Nothing in the queue!')
    else:
        Embed = discord.Embed(title='Queue for ' + ctx.guild.name)
        queueTracker = 1
        for i in players[id]:
            if (queueTracker > 10):
                break
            currentURL = 'https://www.youtube.com/watch?v=' + i[0].id
            Embed.add_field(name=str(queueTracker) + '.', value='[%s](%s)' % (i[0].title, currentURL), inline=False)
            queueTracker += 1
            
        
        await ctx.send(embed=Embed)


@bot.command(name='np')
async def np(ctx):
    guildID = ctx.guild.id
    player = players[guildID][0][0]
    minuteLength = player.duration // 60
    secondLength = player.duration % 60
    hourLength = 0
    if (minuteLength >= 60):
        hourLength = minuteLength // 60
        minuteLength = minuteLength % 60
        
    
    Embed = None
    if (hourLength == 0):
        Embed = discord.Embed(title=player.title, description='Requested by ' + ctx.author.name + ' (Duration of ' + str(minuteLength) + ':' + str(secondLength) + ')', colour=discord.Colour.red(), url='https://www.youtube.com/watch?v=' + player.id)
    else:
        Embed = discord.Embed(title=player.title, description='Requested by ' + ctx.author.name + ' (Duration of ' + str(hourLength) + ':' + str(minuteLength) + ':' + str(secondLength) + ')', colour=discord.Colour.red(), url='https://www.youtube.com/watch?v=' + player.id)
        
    Embed.set_author(name='Now playing...')
    
    await ctx.send(embed=Embed)
#bot.wait_for (Quiz Time)



bot.run(TOKEN)


