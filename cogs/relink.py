# MIT License
# Copyright (c) 2019-2020 Fyssion
# See LICENSE for license details

from discord.ext import commands
import discord

import re
from .utils.utils import (
    wait_for_deletion,
    check_for_help,
    is_opted_out,
    add_to_statistics,
    is_wosh_detector,
)


class Relink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = self.bot.reddit

    def regex(self, message, letter):
        args = message.split(f"{letter}/")
        afterSlash = " ".join(args[1:])
        args = afterSlash.split(" ")
        usr = " ".join(args[0:1])

        # Replaces listed characters with a blank
        usr = re.sub("""[!\.\?\-\'\"\*]""", "", usr)

        return usr

    def link_detector(self, message, letter):
        """Extremely simple algorithm that detects if 'u/' was found in a message and finds the text directly after."""

        urls = re.findall(
            "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
            message,
        )  # Finds all urls in the message

        if (
            len(urls) > 0
        ):  # If the message has any urls, the bot doesnt relink the subreddit
            return

        if message.startswith(f"{letter}/") or message.startswith(f"/{letter}/"):
            return self.regex(message, letter)

        if f" {letter}/" in message or f" /{letter}/" in message:
            return self.regex(message, letter)

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
        args = user.icon_img.split("?")
        icon = args[0]
        em.set_thumbnail(url=icon)
        em.set_footer(text=self.bot.auto_deletion_message)

        bot_message = await message.channel.send(embed=em)
        self.bot.loop.create_task(
            wait_for_deletion(
                bot_message, user_ids=(message.author.id,), client=self.bot
            )
        )

    async def redditor_not_found(self, message, usr):
        """
        Sends an embed saying the redditor does not exist.
        """

        msg = f":warning: Redditor `{usr}` does not exist.{check_for_help(usr) or ''}"

        msg += "\n\n" + self.bot.optout_message

        em = discord.Embed(description=msg, color=self.bot.warning_color)

        await message.channel.send(embed=em, delete_after=7)

    @commands.Cog.listener("on_message")
    async def redditor_relinker(self, message):
        if is_opted_out(message.author, self.bot):
            return

        usr = self.link_detector(message.content, "u")

        if usr is not None:
            # Reddit's user search is absolute trash. It only shows users with 50+ followers.
            # This is my solution
            user = await self.reddit.fetch_redditor(usr)

            add_to_statistics(self.bot, "redditor")

            if user:
                await self.display_redditor(message, user)

            else:
                await self.redditorNotFound(message, usr)

    def subreddit_link_detector(self, message):
        """Extremely simple algorithm that detects if 'r/' was found in a message and finds the text directly after."""

        urls = re.findall(
            "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
            message,
        )  # Finds all urls in the message

        # If the message has any urls, the bot doesnt relink the subreddit
        if len(urls) > 0:
            return

        if message.startswith("r/") or message.startswith("/r/"):
            return self.regex_subreddit(message)

        if " r/" in message or " /r/" in message:
            return self.regex_subreddit(message)

    async def display_subreddit(self, message, subreddit):
        """
        Basically fetches the subreddit, creates the embed, and sends it.
        """

        if subreddit.over18 == True:
            isNSFW = "\n:warning:Subreddit is NSFW!:warning:"
        else:
            isNSFW = ""

        description = f"[r/{subreddit.display_name}](https://reddit.com/r/{subreddit.display_name})\
            \n{subreddit.public_description}{isNSFW}{self.ifIsWosh}{check_for_help(subreddit.display_name) or ''}"

        description += "\n\n" + self.bot.optout_message

        em_url = f"https://reddit.com/r/{subreddit.display_name}"

        em = discord.Embed(
            title=subreddit.title,
            description=description,
            url=em_url,
            color=self.bot.reddit_color,
        )

        em.add_field(name="Subscribers:", value=str(subreddit.subscribers))

        # The next if/else statements are a bug patch. Sometimes, subreddit.icon_img returns None instead of a blank string.
        # Disocrd will not accept this as a url, so I change None to a blank string
        if not subreddit.icon_img:
            subIcon = ""
        else:
            subIcon = subreddit.icon_img

        em.set_thumbnail(url=subIcon)
        em.set_footer(text=self.bot.auto_deletion_message)

        bot_message = await message.channel.send(embed=em)
        self.bot.loop.create_task(
            wait_for_deletion(
                bot_message, user_ids=(message.author.id,), client=self.bot
            )
        )

    async def subreddit_not_found(self, message, sub):
        """
        Sends an embed saying the subreddit does not exist.
        """

        msg = f":warning: Subreddit `{sub}` does not exist.{self.ifIsWosh}{check_for_help(sub) or ''}"

        msg += "\n\n" + self.bot.optout_message

        em = discord.Embed(description=msg, color=self.bot.warning_color)

        await message.channel.send(embed=em, delete_after=7)

    @commands.Cog.listener("on_message")
    async def subreddit_relinker(self, message):
        if is_opted_out(message.author, self.bot):
            return

        sub = self.link_detector(message.content, "r")

        if sub is not None:
            self.ifIsWosh = is_wosh_detector(sub)

            # Searching for subreddit to see if it exists
            subreddit = await self.reddit.fetch_subreddit(sub)

            add_to_statistics(self.bot, "subreddit")

            if subreddit:
                await self.display_subreddit(message, subreddit)

            else:
                await self.subreddit_not_found(message, sub)


def setup(bot):
    bot.add_cog(Relink(bot))
