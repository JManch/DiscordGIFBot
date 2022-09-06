# DiscordGIFBot
![version](https://img.shields.io/github/v/tag/JManch/DiscordGIFBot?label=version)

A simple discord bot that stores a database of GIF URLs and posts a GIF when the relevant keyword is used. Aims to fix the problem of having a long list of favourited GIFs that is annoying to scroll through.

## Usage

- Although the bot is intended to be used for GIFs, it can be used for any media in the form of a URL
- A list of bot commands can be viewed by typing `gifhelp`
- The GIF database is stored in the script's directory as `db.json`
- A single bot can be used across multiple servers. Each server will have their own GIFs.

## Limitations

When a user mentions a GIF and it is posted, the GIF would ideally combine with the user's original message rather than creating a gap between the bot's message and the user's. Unfortunately, the discord API does not allow bots to edit messages or post messages as a user.

To get around this the bot will delete the user's original message containing the GIF and post it again as themselves, including the GIF. The first line of the bot's message will contain the message poster's name in bold. It's not an ideal solution but it's the best I could come up with given the API limitations.

## Self-Hosting

To self-host the bot you must have Python version 3.10 or newer installed.
1. Create and activate a python virtual environment (optional but recommended)
2. Run the command `pip install -r requirements.txt`
3. Create a file called .env and add `TOKEN=INSERT_TOKEN_HERE` to the first line
4. Launch the bot with `python3 gif_bot.py` or optionally use the linux scripts start.sh and stop.sh to run it in the background
