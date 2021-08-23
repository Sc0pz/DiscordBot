from discord.ext import commands
import discord
import main

class Invites(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command(pass_context=True)
    async def invites(self, ctx, *args):
        #Grab all invites in server
        invitesList = await ctx.guild.invites()
        Embed = discord.Embed(title='Invites:', colour=discord.Colour.dark_green())
        #If invites is zero (not possible!!!) send message, otherwise go as normal
        if (len(invitesList) == 0):
            Embed.description = 'No invites active.'
            await ctx.send(embed=Embed)
            return
        else:
            #invitePage of 0 = page 1 default
            invitePage = 0
            #Attempts to grab page argument, if it fails treat
            #the command as if getting page 1 of invites
            try:
                invitePage = int(args[0])
                invitePage -= 1
                if (invitePage < 0): invitePage = 0
            except:
                #Nothing to do if an exception arises
                pass
            #Each page contains a maximum of 5 invites, 
            #index starts as a multiple of 5
            invitePage *= 5
            if (invitePage > len(invitesList)):
                #Invite page cannot exceed number of invites
                await ctx.send('Invalid page given!')
                return
            #Indicates where to stop loop of getting invites
            inviteEnd = invitePage + 5
            if (inviteEnd > len(invitesList)): inviteEnd = len(invitesList) #If page given is the last page
            Embed.set_footer(text=f'Page {int((invitePage / 5) + 1)}/{int((inviteEnd / 5) + 1)} • Type ,invites [page] to go to [page] of invites')
            #Grabs all invites in page based on previous variables, using invitePage as start and inviteEnd as the end
            for i in range(invitePage, inviteEnd):
                dateCreated = invitesList[i].created_at
                inviteAuthor = invitesList[i].inviter.name + "#" + str(invitesList[i].inviter.discriminator)
                embedValue = "Date Created: " + str(dateCreated)[:10] + "\n Creator: " + str(inviteAuthor)
                Embed.add_field(name=invitesList[i].url, value=embedValue, inline=False)
        
        await ctx.send(embed=Embed)
    
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def revokeinvite(self, ctx, *args):
        #Must have one argument ONLY provided
        if (len(args) != 1):
            await ctx.send('Invalid number of arguments! Please paste the invite link *only.*')
            return
        try:
            #Attempts to grab invite and deletes it based on the given argument.
            revokedInvite = await self.bot.fetch_invite(args[0])
            await revokedInvite.delete()
            await ctx.send(f'The invite `{args[0]}` was successfully deleted.')
        except:
            await ctx.send('The invite was unable to be deleted (Is the invite valid?).')
    
    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        discordServer = invite.guild
        inviteChannel = None
        #Snippet grabs channel to send invite to from database
        data = main.db['log_channels'].find_one(
            {
                "guild_id": discordServer.id,
                "log_type": 2
            }
        )
        if data is None:
            #Only executes if no channel has been set in the database (SHOULD BE REMOVED)
            print('No channel has been set!')
        else:
            inviteChannel = await self.bot.fetch_channel(data["channel_id"])
        #Grabs information from the created invite
        inviteAuthor = str(invite.inviter.name) + '#' + str(invite.inviter.discriminator)
        dateCreated = invite.created_at
        try:
            #Loops through all channels in the current guild/server to find the channel to send the message to
            for i in range(len(discordServer.text_channels)):
                if (discordServer.text_channels[i].name.lower() == inviteChannel.name):
                    Embed = discord.Embed(title='New invite created', description='Invite Link: ' + str(invite.url) + '\n Date Created: ' + str(dateCreated)[:10] + '\n Time Created: ' + str(dateCreated)[11:19] + ' UTC', colour=discord.Colour.dark_green())
                    Embed.set_author(name=inviteAuthor, icon_url=str(invite.inviter.avatar_url))
                    await discordServer.text_channels[i].send(embed=Embed)
                    return
        except:
            print("An error occurred in sending the embed")

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def inviteinfo(self, ctx, *args):
        #Must have one argument ONLY provided
        invite = None
        if (len(args) != 1):
            await ctx.send('Invalid number of arguments! Please paste the invite link *only.*')
            return
        try:
            invite = await self.bot.fetch_invite(args[0])
            #Grabs actual invite object from looping through all invites
            #in the current server (fetch_invite does not give invite object with all metadata)
            for i in (await ctx.guild.invites()):
                if (invite.url == i.url):
                    invite = i
                    break
        except:
            await ctx.send('Unable to fetch the invite (Is the invite valid?).')
            return
        dateCreated = invite.created_at
        #Embed Generation that adds most of the invite attributes/information
        Embed = discord.Embed(title=invite.url, colour=discord.Colour.dark_green())
        Embed.set_author(name=f'{invite.inviter.name}#{invite.inviter.discriminator}', icon_url=str(invite.inviter.avatar_url))
        Embed.add_field(name='Channel:', value=f'#{invite.channel.name}')
        Embed.add_field(name='Date Created:', value=str(dateCreated)[:10], inline=False)
        Embed.add_field(name='Time created:', value=f'{str(dateCreated)[11:19]} UTC', inline=False)
        maxUses = invite.max_uses
        if (maxUses == 0): maxUses = 'Infinite'
        Embed.add_field(name='Uses:', value=f'{invite.uses}/{maxUses} total uses.', inline=False)
        
        #invite.max_age is static and does not update, removed block
        #timeLeftSeconds = invite.max_age
        #if (timeLeftSeconds == 0):
        #    Embed.add_field(name='Expires in:', value='Never')
        #else:
        #    timeLeftDays = timeLeftSeconds / 86400
        #    timeLeftSeconds %= 86400
        #    timeLeftHours = timeLeftSeconds / 3600
        #    timeLeftSeconds %= 3600
        #    timeLeftMinutes = timeLeftSeconds / 60
        #    timeLeftSeconds %= 60
        #    Embed.add_field(name='Expires in:', value=f'{int(timeLeftDays)} days, {int(timeLeftHours)} hours, {int(timeLeftMinutes)} minutes, {int(timeLeftSeconds)} seconds.')

        await ctx.send(embed=Embed)
        
    #Exception handling catches MissingPermissions error and notifies the user they don't have the permissions for these commands.    
    @inviteinfo.error
    @revokeinvite.error
    @invites.error
    async def inviteserror(self, ctx, error):
        #await ctx.send(type(error))
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You are missing Administrator permission(s) to run this command.")

def setup(bot):
    bot.add_cog(Invites(bot))