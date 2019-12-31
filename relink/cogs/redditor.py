# MIT License
# Copyright (c) 2019-2020 Fyssion
# See LICENSE for license details

from discord.ext import commands
import discord

import prawcore

import re
from .utils import wait_for_deletion, checkForHelp

class Redditor(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.log = self.bot.log
        self.reddit = self.bot.reddit

    

    def redditorLinkDetector(self, message):
        """Extremely simple algorithm that detects if 'u/' was found in a message and finds the text directly after."""
    
        def findRedditor(message):
            args = message.split("u/")
            afterSlash = " ".join(args[1:])
            args = afterSlash.split(" ")
            usr = " ".join(args[0:1])

            usr = re.sub('''[!\.\?\-\'\"\*]''','', usr) # Replaces listed characters with a blank

            return usr

        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message) # Finds all urls in the message

        if len(urls) > 0: # If the message has any urls, the bot doesnt relink the subreddit
            return
        
        if message.startswith("u/") or message.startswith("/u/"):

            return findRedditor(message)
        
        if " u/" in message or " /u/" in message:

            return findRedditor(message)

    
    async def findRedditor(self, message, usr):
        """
        Basically fetches the redditor, creates the embed, and sends it.
        """

        user = self.reddit.redditor(usr)

        if user.is_employee == True:
            emp = " <:employee:634152137445867531>\nThis user is a Reddit employee."
        else:
            emp = ""
        
        karma = user.comment_karma + user.link_karma
        description = f"[u/{user.name}](https://reddit.com/u/{user.name}){emp}{checkForHelp(usr) or ''}"
        url = f"https://reddit.com/u/{user.name}"
            


        em = discord.Embed(
            title = user.name,
            description=description, url = url,
            color = self.bot.reddit_color
            )
        em.add_field(
            name = "Karma:",
            value = str(karma)
            )
        em.set_thumbnail(url = user.icon_img)
        em.set_footer(text = self.bot.auto_deletion_message)

        try:
            bot_message = await message.channel.send(embed=em)
            self.bot.loop.create_task(
                wait_for_deletion(bot_message, user_ids=(message.author.id,), client=self.bot)
            )
        except discord.errors.Forbidden:
            self.log.error(f"Bot does not have permission to send messages in channel: '{str(message.channel)}'")

    
    async def redditorNotFound(self, message, usr):
        """
        Sends an embed saying the redditor does not exist.
        """

        self.log.warning(f"Redditor '{usr}' does not exist!")

        msg = f":warning: Redditor `{usr}` does not exist.{checkForHelp(usr) or ''}"

        em = discord.Embed(
            description = msg,
            color = self.bot.warning_color
            )
            
        try:
            await message.channel.send(embed=em, delete_after = 7)
        except discord.errors.Forbidden:
            self.log.error(f"Bot does not have permission to send messages in channel: '{str(message.channel)}'")


    @commands.Cog.listener()
    async def on_message(self, message):

        usr = self.redditorLinkDetector(message.content)

        if usr is not None:
            
            self.log.info(str(message.author) + " tried to link to '" + usr + "'")
            
            # Reddit's user search is absolute trash. It only shows users with 50+ followers.
            # This is my solution
            user = self.reddit.redditor(usr)
            try:
                user.link_karma # This throws an error if the user does not exist
                isValidUser = True
            except prawcore.exceptions.NotFound:
                isValidUser = False



            if isValidUser is True:
                await self.findRedditor(message, usr)

                return


            # If the user does not exist
            await self.redditorNotFound(message, usr)



def setup(bot):
    bot.add_cog(Redditor(bot))