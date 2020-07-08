# Reddit ReLink

## Archive Note

I am done maintaining this project, so I have put it in an archived state.
The Reddit ReLink Discord bot will no longer be online.
However, if you wish to use the bot yourself, there are hosting instrucitons below.
Please note that the source code may become very quickly outdated due to changes with Discord.

## Invite ReLink [![Discord Bots](https://top.gg/api/widget/status/618868626945998849.svg)](https://top.gg/bot/618868626945998849)

[Invite Reddit ReLink to your server!](https://discordapp.com/api/oauth2/authorize?client_id=618868626945998849&permissions=18432&scope=bot)

## Info

Reddit ReLink is a Discord bot that relinks Subreddit 'links' users have sent.

Reddit ReLink currently relinks subreddits (`r/SUBREDDIT`) and users (`u/USER`).

Mention the bot for some basic info and a link back to here.

‍

**To globally opt out of ReLink, use `@Reddit ReLink#1038 optout`**

You can opt back in with `@Reddit ReLink#1038 optin`

‍

Every message the bot sends automatically deletes after 30 seconds.

If you want to delete the message sooner, just click the ❌ reaction.

If you want to keep the message, just react with 📌, and the bot won't delete it.

‍

For example:

![Example](https://i.imgur.com/v6ZyNi3.png)

## Libraries

discord.py - [Docs](https://discordpy.readthedocs.io) | [GitHub](https://github.com/Rapptz/discord.py) | [Discord Server](https://discord.gg/r3sSKJJ)

aiohttp - [Docs](https://docs.aiohttp.org/en/stable/) | [GitHub](https://github.com/aio-libs/aiohttp)

PyYAML - [Docs](https://pyyaml.org/) | [GitHub](https://github.com/yaml/pyyaml)

## Install/Requirements

I would rather you just invite Reddit ReLink to your server,
but if you really want to host it yourself, here are the instructions:

**You must install Python and these libraries to run the bot.**

Install Python 3.7+

Install the following libraries with PyPI (pip) OR install from `requirements.txt`:

- `discord.py>=1.2.5`

- `pyyaml`

- `async_timeout`

- OPTIONAL: `jishaku` [What's this?](https://github.com/Gorialis/jishaku)

Next, clone the repository.

Create and fill in a `config.yml` file with the required items.

Example:

```yml
# In a file called config.yml:
discord_token: "DISCORD-TOKEN-HERE"
```

Run `bot.py`.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
