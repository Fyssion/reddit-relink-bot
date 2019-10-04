# Written by incompetenator
# https://www.github.com/incompetenator

# Libraries
import discord
import praw
import coloredlogs, logging


# Colored logs install
l = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=l, fmt='(%(asctime)s) %(levelname)s %(message)s', datefmt='%H:%M:%S')


# Reddit PRAW login
reddit = praw.Reddit(client_id='REDACTED',
                     client_secret='REDACTED',
                     user_agent='my user agent')


# Discord.py client
client = discord.Client()


# Variables
TOKEN = "REDACTED"
reddit_ex = "r/"
reddit_ex2 = "/r/"
BOT_NAME = "Reddit ReLink"
VERSION_NUMBER = "0.1.0"
ICON = "https://cdn.discordapp.com/attachments/402518339215294471/629138727322517507/user-interface-36-512.png"
isnsfw = ""
wosh = ""
reddit_color = 0xFF4301
hyperlink_color = 0x3366BB # Not used
warning_color = 0xFFCC4D
issub = False


# The ReLinking Begins!
@client.event
async def on_message(message):
    global isnsfw
    global wosh
    global issub
    if reddit_ex in message.content: # My stupid detection system (I'm too lazy to rewrite it)
        args = message.content.split("r/")
        afterslash = " ".join(args[1:])
        args = afterslash.split(" ")
        sub = " ".join(args[0:1])

        l.info(str(message.author) + " tried to link to Subreddit " + sub + ".")

        wosh = ""

        # My solution for people linking 'wosh' (or any other varient of 'woooosh')
        if sub == "whosh" or sub == "wosh" or sub == "whoosh" or sub == "whooosh" or sub == "woosh" or sub == "wooosh"  or "oooo" in sub or "wosh" in sub or "whosh" in sub and sub != "woooosh":
            wosh = "\nLooking for [r/woooosh](https://reddit.com/r/woooosh)?"

        # The next next two if statements detect if the subreddit is NSFW by first including NSFW subs in the search, then not.
        # If the subreddit is NSFW, then the 2nd if statement will not run.
        subreddit_search = reddit.subreddits.search_by_name(sub, include_nsfw=True, exact=False)
        if sub in subreddit_search:
            isnsfw = "\n:warning:Subreddit is NSFW!:warning:"
            issub = True

        subreddit_search2 = reddit.subreddits.search_by_name(sub, include_nsfw=False, exact=False)
        if sub in subreddit_search2:
            isnsfw = ""
            issub = True

        # If the subreddit is not found in any searches
        else:
            em_title = ":warning:Subreddit not found!"
            em_disc = "r/" + sub + " is not a subreddit." + isnsfw + wosh
            em = discord.Embed(title = em_title, description = em_disc, color=warning_color)
            em.set_footer(text = str(BOT_NAME) + " • Version " + VERSION_NUMBER, icon_url = ICON)
            await message.channel.send(embed=em)
            l.warning("Subreddit '" + sub + "' does not exist!")
            issub = False

        # Fetches subreddit's name and display name only if subreddit was found in search
        if issub == True:
            subreddit = reddit.subreddit(sub)

            em_sub_title = "[r/" + subreddit.display_name + "](https://reddit.com/r/" + subreddit.display_name + ")" + isnsfw + wosh
            em_title = subreddit.title
            em_url = "https://reddit.com/r/" + subreddit.display_name
            em = discord.Embed(title = em_title, description=em_sub_title, url = em_url, color=reddit_color)
            em.set_thumbnail(url = subreddit.icon_img)
            em.set_footer(text = str(BOT_NAME) + " • Version " + VERSION_NUMBER, icon_url = ICON)
            await message.channel.send(embed=em)

    # If the bot gets mentioned
    elif client.user.mentioned_in(message) and message.mention_everyone is False:
            l.info("Mentioned by " + str(message.author))
            em_title = "Hey there, " + message.author.mention + "! I'm a bot that detects any Reddit links and relinks them in clickable fashion!\n[Visit my GitHub for more info.](https://github.com/incompetenator/discord-relink)"
            em = discord.Embed(description=em_title, color=0xFFFFFF)
            em.set_footer(text = str(BOT_NAME) + " • Version " + VERSION_NUMBER, icon_url = ICON)
            await message.channel.send(embed=em)

            
            
        

# Bot is ready message (not the same as logged in)
@client.event
async def on_ready():
    l.info("\nLogged in as\n" + client.user.name + "\n" + str(client.user.id) + "\n------")

    # Set bot's activity (some call it status) to "Watching Reddit"
    activity = discord.Activity(name="Reddit", type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)

# Runs bot (it's not rocket science)
client.run(TOKEN)
