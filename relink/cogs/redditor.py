from discord.ext import commands
import discord

import prawcore

import re

from .utils import wait_for_deletion

class Redditor(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.log = self.bot.log
        self.reddit = self.bot.reddit


    
    async def findRedditor(self, message, usr):
        user = self.reddit.redditor(usr)

        if user.is_employee == True:
            emp = " <:employee:634152137445867531>\nThis user is a Reddit employee."
        else:
            emp = ""
        
        karma = user.comment_karma + user.link_karma
        description = f"[u/{user.name}](https://reddit.com/u/{user.name}){emp}"
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

        title = ":warning: User not found!"
        description = f"r/{usr} is not a redditor."


        em = discord.Embed(
            title = title,
            description = description,
            color = self.bot.warning_color
            )

        em.set_footer(
            text = self.bot.auto_deletion_message
            )

        self.log.warning(f"Redditor '{usr}' does not exist!")
            
        try:
            bot_message = await message.channel.send(embed=em)
            self.bot.loop.create_task(
                wait_for_deletion(bot_message, user_ids=(message.author.id,), client=self.bot)
            )
        except discord.errors.Forbidden:
            self.log.error(f"Bot does not have permission to send messages in channel: '{str(message.channel)}'")


    @commands.Cog.listener()
    async def on_message(self, message):
        msg = message.content

        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', msg) # Finds all urls in the message

        if len(urls) > 0: # If the message has any urls, the bot doesnt relink the subreddit
            return



        if "u/" in msg: # My stupid detection system (I'm too lazy to rewrite it)
            args = message.content.split("u/")
            afterslash = " ".join(args[1:])
            args = afterslash.split(" ")
            usr = " ".join(args[0:1])

            usr = re.sub('''[!\.\?\-\'\"\*]''','',usr) # Replaces listed characters with a blank

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