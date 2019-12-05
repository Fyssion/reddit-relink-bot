import asyncio
import contextlib
from discord.ext import commands
import discord
from discord import Client, Embed, File, Member, Message, Reaction, TextChannel, Webhook
from discord.abc import Snowflake
from typing import Optional, Sequence, Union


async def wait_for_deletion(
    message: Message,
    user_ids: Snowflake,
    deletion_emoji: str = '❌',
    timeout: int = 30,
    attach_emojis: bool = True,
    client: Optional[Client] = None
) -> None:
    """
    Wait for up to `timeout` seconds for a reaction by any of the specified `user_ids` to delete the message.
    An `attach_emojis` bool may be specified to determine whether to attach the given
    `deletion_emojis` to the message in the given `context`
    A `client` instance may be optionally specified, otherwise client will be taken from the
    guild of the message.
    """
    if message.guild is None and client is None:
        raise ValueError("Message must be sent on a guild")

    bot = client or message.guild.me

    if attach_emojis:
        
        await message.add_reaction(deletion_emoji)

    def check(reaction: Reaction, user: Member) -> bool:
        """Check that the deletion emoji is reacted by the approprite user."""
        return (
            reaction.message.id == message.id
            and reaction.emoji == deletion_emoji
            and user.id in user_ids
        )

    # with contextlib.suppress(asyncio.TimeoutError):
    #     await bot.wait_for('reaction_add', check=check, timeout=timeout)
    #     await message.delete()
    try:
        await bot.wait_for('reaction_add', check=check, timeout=timeout)
        await message.delete()
    except asyncio.TimeoutError:
        
        await message.delete()
    #     # await message.remove_reaction(deletion_emoji, discord.Object(bot.user.id))