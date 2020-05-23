# MIT License
# Copyright (c) 2019-2020 Fyssion
# See LICENSE for license details

from discord.ext import commands
import discord

import prawcore

import re
from .utils.utils import (
    wait_for_deletion,
    check_for_help,
    is_opted_out,
    add_to_statistics,
)


class Redditor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = self.bot.log
        self.reddit = self.bot.reddit

    def regex_redditor(self, message):
        args = message.split("u/")
        afterSlash = " ".join(args[1:])
        args = afterSlash.split(" ")
        usr = " ".join(args[0:1])

        usr = re.sub(
            """[!\.\?\-\'\"\*]""", "", usr
        )  # Replaces listed characters with a blank

        return usr

    def redditor_link_detector(self, message):
        """Extremely simple algorithm that detects if 'u/' was found in a message and finds the text directly after."""

        urls = re.findall(
            "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
            message,
        )  # Finds all urls in the message

        if (
            len(urls) > 0
        ):  # If the message has any urls, the bot doesnt relink the subreddit
            return

        if message.startswith("u/") or message.startswith("/u/"):
            return self.regex_redditor(message)

        if " u/" in message or " /u/" in message:
            return self.regex_redditor(message)

    async def display_redditor(self, message, user):
        """
        Basically fetches the redditor, creates the embed, and sends it.
        """

        if user.is_employee == True:
            emp = " <:employee:634152137445867531>\nThis user is a Reddit employee."
        else:
            emp = ""

        karma = user.comment_karma + user.link_karma
        description = f"[u/{user.name}](https://reddit.com/u/{user.name}){emp}{check_for_help(user.name) or ''}"
        url = f"https://reddit.com/u/{user.name}"

        description += "\n\n" + self.bot.optout_message

        em = discord.Embed(
            title=user.name,
            description=description,
            url=url,
            color=self.bot.reddit_color,
        )
        em.add_field(name="Karma:", value=str(karma))
        em.set_thumbnail(url=user.icon_img)
        em.set_footer(text=self.bot.auto_deletion_message)

        bot_message = await message.channel.send(embed=em)
        self.bot.loop.create_task(
            wait_for_deletion(
                bot_message, user_ids=(message.author.id,), client=self.bot
            )
        )

    async def redditorNotFound(self, message, usr):
        """
        Sends an embed saying the redditor does not exist.
        """

        self.log.warning(f"Redditor '{usr}' does not exist!")

        msg = f":warning: Redditor `{usr}` does not exist.{check_for_help(usr) or ''}"

        msg += "\n\n" + self.bot.optout_message

        em = discord.Embed(description=msg, color=self.bot.warning_color)

        await message.channel.send(embed=em, delete_after=7)

    @commands.Cog.listener("on_message")
    async def on_redditor(self, message):
        if is_opted_out(message.author, self.bot):
            return

        usr = self.redditor_link_detector(message.content)

        if usr is not None:

            self.log.info(str(message.author) + " tried to link to '" + usr + "'")

            # Reddit's user search is absolute trash. It only shows users with 50+ followers.
            # This is my solution
            user = await self.reddit.fetch_redditor(usr)

            add_to_statistics(self.bot, "redditor")

            if user:
                await self.display_redditor(message, user)

            else:
                await self.redditorNotFound(message, usr)


def setup(bot):
    bot.add_cog(Redditor(bot))
