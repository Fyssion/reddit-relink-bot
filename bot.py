# Written by incompetenator
# https://www.github.com/incompetenator

# Libraries
import discord
import praw
import coloredlogs, logging
import yaml
import re


# Colored logs install
l = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=l, fmt='(%(asctime)s) %(levelname)s %(message)s', datefmt='%H:%M:%S')


#Config.yml load
with open("config.yml", 'r') as config:
    try:
        data = yaml.safe_load(config)

    except yaml.YAMLError as exc:
        l.critical("Could not load config.yml")
        print(exc)


# Reddit PRAW login
reddit = praw.Reddit(client_id = data['reddit_client_id'],
                     client_secret = data['reddit_client_secret'],
                     user_agent = 'my user agent')

if reddit.read_only == True:
    l.info("Logged into Reddit")


# Discord.py client
client = discord.Client()


# Variables
TOKEN = data['discord_token']
reddit_ex = "r/"
reddit_ex2 = "/r/"
BOT_NAME = "Reddit ReLink"
VERSION_NUMBER = "0.3.0"
ICON = "https://media.discordapp.net/attachments/402518339215294471/631655810048589845/icon.png?width=449&height=449"
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

    # Direct Link Detection
    msg = message.content
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', msg) # Finds all urls in the message

    if len(urls) > 0: # If the message has any urls, the bot doesnt relink the subreddit
        msg = ""


    if reddit_ex in msg: # My stupid detection system (I'm too lazy to rewrite it)
        args = message.content.split("r/")
        afterslash = " ".join(args[1:])
        args = afterslash.split(" ")
        sub = " ".join(args[0:1])

        sub = re.sub('''[!\.\?\-\'\"\*]''','',sub) # Replaces listed characters with a blank

        l.info(str(message.author) + " tried to link to '" + sub + "'")

        wosh = ""

        # My solution for people linking 'wosh' (or any other varient of 'woooosh')
        if sub == "whosh" or sub == "wosh" or sub == "whoosh" or sub == "whooosh" or sub == "woosh" or sub == "wooosh"  or "oooo" in sub or "wosh" in sub or "whosh" in sub and sub != "woooosh":
            if sub != "woooosh":
                wosh = "\nLooking for [r/woooosh](https://reddit.com/r/woooosh)?"

        # Searching for subreddit to see if it exists
        subreddit_search = reddit.subreddits.search_by_name(sub, include_nsfw=True, exact=False)
        if sub in subreddit_search:
            isnsfw = "\n:warning:Subreddit is NSFW!:warning:"
            issub = True


        # If the subreddit is not found in any searches
        if issub == False:
            em_title = ":warning:Subreddit not found!"
            em_disc = "r/" + sub + " is not a subreddit." + isnsfw + wosh
            em = discord.Embed(title = em_title, description = em_disc, color=warning_color)
            em.set_footer(text = str(BOT_NAME) + " • Version " + VERSION_NUMBER, icon_url = ICON)
            l.warning("Subreddit '" + sub + "' does not exist!")
            
            try:
                await message.channel.send(embed=em)
            except discord.errors.Forbidden:
                l.error("Bot does not have permission to send messages in channel: '" + str(message.channel) + "'")
            
            issub = False
            isnsfw = ""

        # Fetches subreddit's name and display name only if subreddit was found in search
        elif issub == True:
            subreddit = reddit.subreddit(sub)

            if subreddit.over18 == True:
                isnsfw = "\n:warning:Subreddit is NSFW!:warning:"
            else:
                isnsfw = ""
            
            em_sub_title = "[r/" + subreddit.display_name + "](https://reddit.com/r/" + subreddit.display_name + ")\n" + subreddit.public_description + isnsfw + wosh
            em_title = subreddit.title
            em_url = "https://reddit.com/r/" + subreddit.display_name
            em = discord.Embed(title = em_title, description=em_sub_title, url = em_url, color=reddit_color)
            em.add_field(name = "Subscribers:", value = str(subreddit.subscribers))
            em.set_thumbnail(url = subreddit.icon_img)
            em.set_footer(text = str(BOT_NAME) + " • Version " + VERSION_NUMBER, icon_url = ICON)

            try:
                await message.channel.send(embed=em)
            except discord.errors.Forbidden:
                l.error("Bot does not have permission to send messages in channel: '" + str(message.channel) + "'")
            
            issub = False
            isnsfw = ""



    #User relinking
    if "u/" in msg: # My stupid detection system (I'm too lazy to rewrite it)
        args = message.content.split("u/")
        afterslash = " ".join(args[1:])
        args = afterslash.split(" ")
        usr = " ".join(args[0:1])

        usr = re.sub('''[!\.\?\-\'\"\*]''','',usr) # Replaces listed characters with a blank

        l.info(str(message.author) + " tried to link to '" + usr + "'")

        wosh = ""

        # This try/except detects if the user exists
        issub = True
        try:
            user = reddit.redditor(usr)
            tkarma = user.comment_karma + user.link_karma # For some reason this generates an error
        except:
            issub = False

        # If the user does not exist
        if issub == False:
            em_title = ":warning:User not found!"
            em_disc = "u/" + usr + " is not a user." + isnsfw + wosh
            em = discord.Embed(title = em_title, description = em_disc, color=warning_color)
            em.set_footer(text = str(BOT_NAME) + " • Version " + VERSION_NUMBER, icon_url = ICON)
            l.warning("User '" + usr + "' does not exist!")
            
            try:
                await message.channel.send(embed=em)
            except discord.errors.Forbidden:
                l.error("Bot does not have permission to send messages in channel: '" + str(message.channel) + "'")
            
            issub = False
            isnsfw = ""

        # Fetches user and sends info
        elif issub == True:
            user = reddit.redditor(usr)

            if user.is_employee == True:
                emp = " <:employee:634152137445867531>\nThis user is a Reddit employee."
            else:
                emp = ""
            
            tkarma = user.comment_karma + user.link_karma
            em_sub_title = "[u/" + user.name + "](https://reddit.com/u/" + user.name + ")" + isnsfw + emp
            em_title = user.name
            em_url = "https://reddit.com/u/" + user.name
            em = discord.Embed(title = em_title, description=em_sub_title, url = em_url, color=reddit_color)
            em.add_field(name = "Karma:", value = str(tkarma))
            em.set_thumbnail(url = user.icon_img)
            em.set_footer(text = str(BOT_NAME) + " • Version " + VERSION_NUMBER, icon_url = ICON)

            try:
                await message.channel.send(embed=em)
            except discord.errors.Forbidden:
                l.error("Bot does not have permission to send messages in channel: '" + str(message.channel) + "'")
            
            issub = False
            isnsfw = ""



    # If the bot gets mentioned
    elif client.user.mentioned_in(message) and message.mention_everyone is False:
            l.info("Mentioned by " + str(message.author))
            
            em_title = "Hey there, " + message.author.mention + "!\nI'm a bot that detects any Reddit links and relinks them in clickable fashion!\n[Visit my GitHub Repository for more info.](https://github.com/incompetenator/reddit-relink-bot)"
            em = discord.Embed(description=em_title, color=reddit_color)
            em.set_footer(text = str(BOT_NAME) + " • Version " + VERSION_NUMBER, icon_url = ICON)
            try:
                await message.channel.send(embed=em)
            except discord.errors.Forbidden:
                l.error("Bot does not have permission to send messages in channel: '" + str(message.channel) + "'")

            



# Bot is ready message (not the same as logged in)
@client.event
async def on_ready():
    global ICON

    l.info("\nLogged in as\n" + client.user.name + "\n" + str(client.user.id) + "\n------")

    # Set bot's activity (some call it status) to "Watching Reddit"
    activity = discord.Activity(name="Reddit", type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)

    ICON = client.user.avatar_url


# Runs bot (it's not rocket science)
client.run(TOKEN)
