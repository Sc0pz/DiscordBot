from discord.ext import commands

class Disconnect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def disconnect(self, ctx):
        voice_client = ctx.author.guild.voice_client
        if (voice_client is not None):
            await voice_client.disconnect(force=False)
            print(f'{bot.voice_clients}')
        else:
            await ctx.send('No voice channel to disconnect from.')

def setup(bot):
    bot.add_cog(Disconnect(bot))