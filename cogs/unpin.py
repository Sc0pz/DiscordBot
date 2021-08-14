from discord.ext import commands

class Unpin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.guild_only()
    @commands.command()
    async def unpin(self, ctx, *args):
        #Grabs values that test is user has permissions in the channel to unpin
        channel_name = ctx.channel.name
        user_roles = ctx.author.roles
        can_pin = False
        #If user has role that matches channel name then allow them to unpin
        for i in range(len(user_roles)):
            if (user_roles[i].name.casefold() == channel_name.casefold()):
                can_pin = True
        if (can_pin == False):
            await ctx.send('You do not have permissions to unpin in this channel!')
            return
        
        #Unpins message if command is a reply to another message
        #Reference not being None indicates the message is replying and thus pinning message
        ifReply = ctx.message.reference
        if ifReply != None:
            try:
                msg = await ctx.channel.fetch_message(ifReply.message_id)
                if (msg.pinned == False):
                    await ctx.send('This message is not pinned!')
                    return
                await msg.unpin()
                await ctx.send('Successfully unpinned the message.')
            except:
                await ctx.send('The message was unable to be unpinned')
            return
        
        #if not a reply - only one argument expected
        if (len(args) != 1):
            await ctx.send('Invalid number of arguments! Please enter the message ID or link *only.*')
            return
        msgID = args[0]
        #Parses passed argument into an integer message ID, except catches if user inputs a link instead
        try:
            msgID = int(args[0])
        except:
            if (msgID.find('https://discord.com/channels/') == -1):
                await ctx.send('Invalid message ID.')
                return
            else:
                msgIDIndex = args[0].rfind('/')
                msgID = int(args[0][msgIDIndex + 1:])
        
        #Try except block attempts to unpin the message, 
        #Generic except block sends message for any errors 
        #that can arise while unpinning
        try:        
            msg = await ctx.channel.fetch_message(msgID)
            if (msg.pinned == False):
                await ctx.send('This message is not pinned!')
                return
            await msg.unpin()
            await ctx.send('Successfully unpinned the message.')
        except:
            await ctx.send('The message was unable to be unpinned.')

def setup(bot):
    bot.add_cog(Unpin(bot))