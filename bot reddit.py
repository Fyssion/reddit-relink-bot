import discord
import praw
import coloredlogs, logging

#--Logger
l = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=l, fmt='(%(asctime)s) %(levelname)s %(message)s', datefmt='%H:%M:%S')

reddit = praw.Reddit(client_id='REDACTED',
                     client_secret='REDACTED',
                     user_agent='my user agent')

client = discord.Client()

#---Variables--
TOKEN = "REDACTED"
reddit_ex = "r/"
reddit_ex2 = "/r/"
BOT_NAME = "Reddit ReLink"
VERSION_NUMBER = "0.1.0"
ICON = "https://cdn.discordapp.com/attachments/402518339215294471/629138727322517507/user-interface-36-512.png"
isnsfw = ""
wosh = ""
reddit_color = 0xFF4301
#hyperlink_color = 0x0645AD
hyperlink_color = 0x3366BB
warning_color = 0xFFCC4D
issub = False

#--Embed--


#--Commands--
@client.event
async def on_message(message):
    global isnsfw
    global wosh
    global issub
    if reddit_ex in message.content:
        args = message.content.split("r/")
        afterslash = " ".join(args[1:])
        args = afterslash.split(" ")
        sub = " ".join(args[0:1])
        l.info(str(message.author) + " tried to link to Subreddit " + sub + ".")


        wosh = ""

        if sub == "whosh" or sub == "wosh" or sub == "whoosh" or sub == "whooosh" or sub == "woosh" or sub == "wooosh"  or "oooo" in sub or "wosh" in sub or "whosh" in sub and sub != "woooosh":
            wosh = "\nLooking for [r/woooosh](https://reddit.com/r/woooosh)?"

        subreddit_search = reddit.subreddits.search_by_name(sub, include_nsfw=True, exact=False)
        if sub in subreddit_search:
            isnsfw = "\n:warning:Subreddit is NSFW!:warning:"
            issub = True

        subreddit_search2 = reddit.subreddits.search_by_name(sub, include_nsfw=False, exact=False)
        if sub in subreddit_search2:
            isnsfw = ""
            issub = True

        else:
            em_title = ":warning:Subreddit not found!"
            em_disc = "r/" + sub + " is not a subreddit." + isnsfw + wosh
            em = discord.Embed(title = em_title, description = em_disc, color=warning_color)
            em.set_footer(text = str(BOT_NAME) + " • Version " + VERSION_NUMBER, icon_url = ICON)
            await message.channel.send(embed=em)
            l.warning("Subreddit '" + sub + "' does not exist!")
            issub = False

        if issub == True:
            subreddit = reddit.subreddit(sub)

            em_sub_title = "[r/" + subreddit.display_name + "](https://reddit.com/r/" + subreddit.display_name + ")" + isnsfw + wosh
            em_title = subreddit.title
            em_url = "https://reddit.com/r/" + subreddit.display_name
            em = discord.Embed(title = em_title, description=em_sub_title, url = em_url, color=reddit_color)
            em.set_thumbnail(url = subreddit.icon_img)
            em.set_footer(text = str(BOT_NAME) + " • Version " + VERSION_NUMBER, icon_url = ICON)
            await message.channel.send(embed=em)


    elif client.user.mentioned_in(message) and message.mention_everyone is False:
            l.info("Mentioned by " + str(message.author))
            em_title = "Hey there, " + message.author.mention + "! I'm a bot that detects any Reddit links and relinks them in clickable fashion!"
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
