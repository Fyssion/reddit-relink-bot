# MIT License
# Copyright (c) 2019-2020 Fyssion
# See LICENSE for license details

from discord.ext import commands
import discord
import logging
import yaml
import re
from datetime import datetime as d
import aiohttp

from cogs.utils.utils import wait_for_deletion
from cogs.utils.aioreddit import RedditClient


file_logger = logging.getLogger("discord")
file_logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="relink.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
file_logger.addHandler(handler)


def get_prefix(client, message):

    prefixes = ["rr!!"]

    return commands.when_mentioned_or(*prefixes)(client, message)


class RedditRelink(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=get_prefix,
            description="A bot that detects any Reddit links and relinks them in clickable fashion.",
            owner_id=224513210471022592,
            case_insensitive=False,
            help_command=None,
        )

        self.log = logging.getLogger("discord")
        self.log.setLevel(logging.INFO)
        self.log.addHandler(logging.StreamHandler())

        # Config.yml load
        with open("config.yml", "r") as config:
            try:
                self.data = yaml.safe_load(config)

            except yaml.YAMLError as exc:
                self.log.critical("Could not load config.yml")
                print(exc)
                quit()

        # Cogs
        self.cogs_to_load = [
            "cogs.relink",
            "cogs.settings",
            "cogs.statistics",
        ]

        # Listeners
        self.add_listener(self.on_mention, "on_message")

        # Other Variables
        self.auto_deletion_message = "This message auto-deletes after 30 seconds."
        self.optout_message = None
        self.reddit_color = 0xFF4301
        self.warning_color = 0xFFCC4D

        self.loop.create_task(self.load_all_cogs())

    async def load_all_cogs(self):
        await self.wait_until_ready()

        try:
            self.load_extension("jishaku")  # For debugging
        except:
            pass

        self.startup_time = d.now()

        self.session = aiohttp.ClientSession(loop=self.loop)
        # Idk what I'm doing wrong with the auth,
        # but reddit returns a forbidden error whenever
        # I try to log in :/
        # self.reddit = RedditClient(
        #     self.data["reddit_client_id"],
        #     self.data["reddit_client_secret"],
        #     session=self.session,
        # )
        self.reddit = RedditClient(session=self.session,)

        for cog in self.cogs_to_load:
            self.load_extension(cog)

    async def on_mention(self, message):
        """
        Responds to a mention with a tiny "help menu."
        It's not really a help menu, and it's not so tiny anymore.
        """

        if (
            message.content == f"<@{self.user.id}>"
            or message.content == f"<@!{self.user.id}>"
        ):

            msg = (
                "Hey there, "
                + message.author.mention
                + "!\nI'm a bot that detects any Reddit links and relinks them in clickable fashion!"
                f"\n\n**To globally opt out of ReLink, use `@{self.user} optout`**\nYou can opt back in with `@{self.user} optin`"
                "\n\nI support relinking subreddits (`r/SUBREDDIT`) and users (`u/USER`)."
                "\n\nEvery message I send (excluding this one) will be automatically deleted after 30 seconds."
                "\nIf you want to delete the message sooner, just click the :x: reaction."
                "\nIf you want to keep the message, just react with :pushpin:, and I'll save it for you."
                "\n\n[Visit my GitHub Repository for more info.](https://github.com/fyssion/reddit-relink-bot)"
            )

            em = discord.Embed(
                description=msg, color=self.reddit_color, timestamp=d.utcnow()
            )
            em.set_footer(text="Reddit ReLink v2.0.0", icon_url=self.user.avatar_url)

            await message.channel.send(embed=em)

    async def logout(self):
        self.session.close()
        await super().logout()

    async def on_ready(self):
        self.log.info(f"Logged in as {self.user.name} - {self.user.id}")

        if self.optout_message is None:
            self.optout_message = f"**Opt out of ReLink with `@{self.user} optout`**"

    def run(self):
        super().run(self.data["discord_token"])


bot = RedditRelink()
bot.run()
