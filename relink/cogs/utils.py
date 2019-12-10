import asyncio
import contextlib
from discord.ext import commands
import discord
from discord import Client, Embed, File, Member, Message, Reaction, TextChannel, Webhook
from discord.abc import Snowflake
from typing import Optional, Sequence, Union


def checkForHelp(msg):
    """
    Check if a subreddit/redditor string contains "help" or "info".
    If it does, return the message below.
    """
    if msg.lower() == "help" or msg.lower() == "info":
        return "\n\n`Looking for some help? Mention me!`"


async def wait_for_deletion(
    message: Message,
    user_ids: Snowflake,
    deletion_emoji: str = '❌',
    pin_emoji: str = "📌",
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
        ifEmojiIsValid = reaction.emoji == deletion_emoji or reaction.emoji == pin_emoji
        return (
            reaction.message.id == message.id
            and ifEmojiIsValid
            and user.id in user_ids
        )

    # with contextlib.suppress(asyncio.TimeoutError):
    #     await bot.wait_for('reaction_add', check=check, timeout=timeout)
    #     await message.delete()
    try:
        addedReaction, userReacting = await bot.wait_for('reaction_add', check=check, timeout=timeout)

        if addedReaction.emoji == pin_emoji:
            
            if message.embeds:
                em = message.embeds[0]
                em.set_footer(text = "Pinned!")
                
                await message.edit(embed = em)


            return await message.remove_reaction(deletion_emoji, discord.Object(bot.user.id))
        
        await message.delete()
            
    except asyncio.TimeoutError:
        
        await message.delete()
    #     # await message.remove_reaction(deletion_emoji, discord.Object(bot.user.id))