# MIT License
# Copyright (c) 2019-2020 Fyssion
# See LICENSE for license details

from discord.ext import commands
import discord

from os import path
import json

from .utils.utils import is_opted_out


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if not path.exists("opted_out.json"):
            with open("opted_out.json", "w") as f:
                json.dump([], f)

        with open("opted_out.json", "r") as f:
            self.bot.opted_out = json.load(f)

    @commands.command(aliases=["opt_out", "nothanks"])
    async def optout(self, ctx):
        if not is_opted_out(ctx.author, self.bot):
            self.bot.opted_out.append(ctx.author.id)
            with open("opted_out.json", "w") as f:
                json.dump(self.bot.opted_out, f)
            return await ctx.send("**:thumbsup: You have been opted out.**")
        else:
            return await ctx.send(
                f"You are already opted out. Use `@{self.bot.user} optin` to opt back in."
            )

    @commands.command(aliases=["opt_in", "yesplease"])
    async def optin(self, ctx):
        if is_opted_out(ctx.author, self.bot):
            self.bot.opted_out.pop(self.bot.opted_out.index(ctx.author.id))
            with open("opted_out.json", "w") as f:
                json.dump(self.bot.opted_out, f)
            return await ctx.send("**:thumbsup: You have been opted in.**")
        else:
            return await ctx.send(
                f"You are opted in. Use `@{self.bot.user} optout` to opt out."
            )


def setup(bot):
    bot.add_cog(Settings(bot))
