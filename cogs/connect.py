from discord.ext import commands

class Connect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def connect(self, ctx):
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

def setup(bot):
    bot.add_cog(Connect(bot))