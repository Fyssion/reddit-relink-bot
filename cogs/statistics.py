# MIT License
# Copyright (c) 2019-2020 Fyssion
# See LICENSE for license details

from discord.ext import commands, tasks
import discord

from datetime import datetime
from os import path
import json


class Statistics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if not path.exists("statistics.json"):
            statistics = {"redditors-relinked": 0, "subreddits-relinked": 0}
            with open("statistics.json", "w") as f:
                json.dump(statistics, f)

        with open("statistics.json", "r") as f:
            self.bot.statistics = json.load(f)

        self.backup.start()

    def cog_unload(self):
        self.backup.cancel()

    @tasks.loop(minutes=5)
    async def backup(self):
        with open("statistics.json", "w") as f:
            json.dump(self.bot.statistics, f)

    @commands.command(
        description="View usage statistics for the bot", aliases=["stats"]
    )
    async def statistics(self, ctx):
        em = discord.Embed(
            title="Usage Statistics",
            color=self.bot.reddit_color,
            timestamp=datetime.utcnow(),
        )

        stats = self.bot.statistics

        em.add_field(
            name="Total ReLinks",
            value=int(stats["redditors-relinked"]) + int(stats["subreddits-relinked"]),
            inline=False,
        )
        em.add_field(
            name="Subreddits Relinked", value=stats["subreddits-relinked"], inline=False
        )
        em.add_field(
            name="Redditors Relinked", value=stats["redditors-relinked"], inline=False
        )

        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Statistics(bot))
