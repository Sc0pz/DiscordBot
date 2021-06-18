from discord.ext import commands

class Pin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def pin(self, ctx, *args):
        #Grabs values that test is user has permissions in the channel to pin
        channel_name = ctx.channel.name
        user_roles = ctx.author.roles
        can_pin = False
        #If user has role that matches channel name then allow them to pin
        for i in range(len(user_roles)):
            if (user_roles[i].name.casefold() == channel_name.casefold()):
                can_pin = True
        if (can_pin == False):
            await ctx.send('You do not have permissions to pin in this channel!')
            return
        
        #Unable to pin if there are 50 or more pinned messages
        pinned_messages = await ctx.channel.pins()
        if (len(pinned_messages) >= 50):
            await ctx.send('This channel has reached the maximum number of pinned messages')
            return
        
        #Pins message if command is a reply to another message
        #Reference not being None indicates the message is replying and thus pinning message
        ifReply = ctx.message.reference
        if ifReply != None:
            try:
                msg = await ctx.channel.fetch_message(ifReply.message_id)
                if (msg.pinned == True):
                    await ctx.send('This message is already pinned!')
                    return
                await msg.pin()
            except:
                await ctx.send('The message was unable to be pinned')
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
                #grabs message ID from given link
                msgIDIndex = args[0].rfind('/')
                msgID = int(args[0][msgIDIndex + 1:])
        #Try except block attempts to pin the message, 
        #Generic except block sends message for any errors 
        #that can arise while pinning
        try:        
            msg = await ctx.channel.fetch_message(msgID)
            if (msg.pinned == True):
                await ctx.send('This message is already pinned!')
                return
            await msg.pin()
        except:
            await ctx.send('The message was unable to be pinned.')

def setup(bot):
    bot.add_cog(Pin(bot))