import discord
import os
import datetime
import pytz
from keep_alive import keep_alive

client = discord.Client()
my_secret = os.environ['token']
# now = datetime.datetime.now()


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author==client.user:
    return 

  if message.content.startswith('$hello'):
    await message.channel.send('Hello')

  if message.content.startswith('$help'):
    await message.channel.send('Maybe Later')

  if message.content.startswith('$about'):
    await message.channel.send('This is a test bot.\nHere are some helpful commands:\n')
    await message.channel.send('Type `$help` for help or `$hello` to greet me!')

  if message.content.startswith('$time'):
    await message.channel.send('The time is: '+datetime.datetime.now(pytz.timezone("America/New_York")).strftime("%d-%b-%Y (%H:%M)"))



keep_alive()

client.run(my_secret)