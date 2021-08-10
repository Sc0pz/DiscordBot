import os
import tempfile
from typing import Union

import discord
from discord.ext import commands

import main
from cogs.banned_words import BannedWords
from utils.database.collections import LOG_CHANNELS

from utils.log_channel_types import LogChannelType


class DeletionDetector(commands.Cog, name="Deletion Detector"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setdeletionlog", aliases=["sdl"])
    @commands.guild_only()
    async def __set_deletion_log_channel(self, ctx: commands.Context, channel: discord.TextChannel):
        """
        **DEPRECATED - USE `channel set` INSTEAD!**

        Set the channel you want deleted messages to be logged to

        Arguments:
            channel: tag the channel you want deleted messages to be logged to
        """
        if ctx.guild.id != channel.guild.id:
            await ctx.reply("The channel must be a text channel from this server!")
            return
        main.db[LOG_CHANNELS].replace_one(
            {
                "guild_id": ctx.guild.id,
                "log_type": LogChannelType.MessageDeletion.value
            },
            {
                "guild_id": ctx.guild.id,
                "log_type": LogChannelType.MessageDeletion.value,
                "channel_id": channel.id
            },
            upsert=True
        )

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.channel.type == discord.ChannelType.group or message.channel.type == discord.ChannelType.private:
            return  # do not log deleted messages in DMs
        channel = \
            await self.bot.get_cog("LoggerChannels").get_channel(self.bot, message.guild.id,
                                                                 LogChannelType.MessageDeletion)
        if channel is None:
            await message.channel.send("No message deletion logging channel was found in this guild!")
            return

        color = discord.Color.red() if (await BannedWords.has_banned_word(message.guild.id, message.content))[0] \
            else discord.Color.orange()
        embed = discord.Embed(title="Deleted Message", color=color)
        embed.set_author(name=f"{message.author.name}#{message.author.discriminator}",
                         icon_url=message.author.avatar.url)
        embed.add_field(name="time sent", value=message.created_at.strftime('%m/%d/%Y - %I:%M %p UTC'), inline=False)
        if isinstance(message.channel, discord.Thread):
            embed.add_field(name="thread", value=f"{message.channel.parent.mention} \u276F {message.channel.mention}")
        else:
            embed.add_field(name="channel", value=message.channel.mention, inline=False)
        attachments: list[discord.File] = []
        temp_name = ""
        if message.content:
            if len(message.content) >= 1024:
                with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp:
                    temp.write(message.content)
                    temp_name = temp.name
                attachments.append(discord.File(fp=temp_name, filename=f"content.txt"))
                content = f"The message was too long, so it has been attached as a text file called " \
                          f"content.txt"
            else:
                content = message.content
            embed.add_field(name="content", value=content, inline=False)
        cdn_links: str = ""
        if message.attachments:
            for attachment in message.attachments:
                file = await attachment.to_file()
                # get the file size
                file.fp.seek(0, os.SEEK_END)
                filesize = file.fp.tell()
                file.fp.seek(0)
                if filesize > message.guild.filesize_limit:
                    attachments.append(discord.File("assets/file_too_big.jpg"))
                else:
                    file.fp.seek(0)
                    attachments.append(file)
                cdn_links += f"[{attachment.filename}]({attachment.url}) ({filesize / 1_048_576.0:.2f}MB)\n"
            embed.add_field(name="attachment URLs (may not always work idk)", value=cdn_links)
        try:
            await channel.send(embed=embed, files=None if not attachments else attachments)
        except discord.errors.HTTPException as e:
            await channel.send(f"ERROR CODE: {e.code}\n"
                               f"MESSAGE: {e}")
        finally:
            # if a temporary file was created for sending a message with large content, delete that file
            if os.path.exists(temp_name):
                os.remove(temp_name)


def setup(bot):
    bot.add_cog(DeletionDetector(bot))
