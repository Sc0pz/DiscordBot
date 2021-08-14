#bot.py
#-----------------------------------------
#Required Packages:
#
#pip install -U discord.py
#pip install -U python-dotenv
#pip install pynacl (I guess)
#pip install -U discord.py[voice] (maybe)
#pip install uwuify
#
#-----------------------------------------
import os
import asyncio
import pymongo
from pymongo import errors

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') 

# connect to database - shamelessly stolen from sumo
try:
    db = pymongo.MongoClient(os.getenv('DB_REMOTE_URL'))["botdb"]
except pymongo.errors.ConfigurationError:
    print("Connecting to the database took too long! Are you connected to the internet?")
    exit(100)

bot = commands.Bot(command_prefix=',')

for f in os.listdir('./cogs'):
    if f.endswith('.py'):
        bot.load_extension(f"cogs.{f[:-3]}")


@bot.event
async def on_ready():
    #Can clean up to be more efficient - changing presence should be done on initialization, not on_ready
    print(f'{bot.user.name} has connected to Discord!')
    print(f'{bot.guilds}')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('in hell'))
      

#TODO: Remove all these commands on release
@bot.command(name='bombito')
async def bombito(ctx):
    Embed = discord.Embed(title='Title', description='Description', colour=discord.Colour.red(), url='https://www.youtube.com/watch?v=yrQgCz_Hr2U')
    stringTest = 'Bombito'
    Embed.add_field(name='bruh', value='[%s](https://www.youtube.com/watch?v=yrQgCz_Hr2U) Im bad' % stringTest)
    await ctx.send(embed=Embed)

@bot.command(name='logoff')
async def logoff(ctx):
    await ctx.send('goodbye')
    exit()

@bot.command(name='honorcode')
async def honorcode(ctx):
    Embed = discord.Embed(title='Honor Code Statement', description='To promote a stronger sense of mutual responsibility, respect, trust, and fairness among all members of the George Mason University Community and with the desire for greater academic and personal achievement, we, the student members of the university community, have set for this Honor Code: Student Members of the George Mason University community pledge not to cheat, plagiarize, steal, or lie in matters related to academic work.', colour = discord.Colour.dark_green())
    await ctx.send(embed=Embed)
    
bot.run(TOKEN)


