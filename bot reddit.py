import discord
from discord.ext import commands
import asyncio
from asyncio import sleep
import praw
import coloredlogs, logging

#--Logger
l = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=l, fmt='(%(asctime)s) %(levelname)s %(message)s', datefmt='%H:%M:%S')

reddit = praw.Reddit(client_id='fRymMJayGXty1g',
                     client_secret='xMt_lwbyy6tMDyYyWZ47zdeyVPY',
                     user_agent='my user agent')

client = discord.Client()

#---Variables--
TOKEN = "NjE4ODY4NjI2OTQ1OTk4ODQ5.XZUb7Q.gMYY_4SQAbnTfarpRGb0DByDGF4"
reddit_ex = "r/"
reddit_ex2 = "/r/"
BOT_NAME = "ReLink"
VERSION_NUMBER = "0.0.1"
ICON = "https://media.discordapp.net/attachments/617425917106716689/617459186175049728/logo.png?width=457&height=457"
MODERATOR_ID = 617730874221527040
MODERATOR_ID_2 = 617730668268617729

#--Embed--


#--Commands--
@client.event
async def on_message(message):
    if reddit_ex in message.content:
        args = message.content.split("r/")
        afterslash = " ".join(args[1:])
        args = afterslash.split(" ")
        sub = " ".join(args[0:1])
        l.info(str(message.author) + " tried to link r/" + sub + ".")
        
        em_title = "[r/" + sub + "](https://reddit.com/r/" + sub + ")"
        em = discord.Embed(description=em_title, color=0xFF4301)
        em.set_footer(text = str(BOT_NAME) + " • Version " + VERSION_NUMBER, icon_url = ICON)
        await message.channel.send(embed=em)

        try:
            subreddit = reddit.subreddit(sub)
            l.debug("Subreddit:")
            l.debug("r/" + subreddit.display_name)  # Output: redditdev
            l.debug("Title:")
            l.debug(subreddit.title)         # Output: reddit Development
            l.debug("Description:")
            l.debug(subreddit.description)   # Output: A subreddit for discussion of ... 
            em_sub_title = "[r/" + subreddit.display_name + "](https://reddit.com/r/" + subreddit.display_name + ")"
            em_title = subreddit.title
            em = discord.Embed(title = em_title, description=em_sub_title, color=0xFF4301)
            em.set_footer(text = str(BOT_NAME) + " • Version " + VERSION_NUMBER, icon_url = ICON)
            await message.channel.send(embed=em)
        except:
            msg = "Failed to get subreddit info. Not a real subreddit?"
            await message.channel.send(msg)


    elif client.user.mentioned_in(message) and message.mention_everyone is False:
            l.info("Mentioned by " + str(message.author))
            em_title = "Hey there, " + message.author.mention + "! I'm a bot that detects any reddit links and relinks them in clickable fashion!"
            em = discord.Embed(description=em_title, color=0xFFFFFF)
            em.set_footer(text = str(BOT_NAME) + " • Version " + VERSION_NUMBER, icon_url = ICON)
            await message.channel.send(embed=em)
            
            
        

#--Bot is ready message--
@client.event
async def on_ready():
    l.info("\nLogged in as\n" + client.user.name + "\n" + str(client.user.id) + "\n------")
    activity = discord.Activity(name="Reddit", type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)
    l.info("Changed activity to 'Reddit'")


client.run(TOKEN)
