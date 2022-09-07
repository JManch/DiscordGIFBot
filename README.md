# DiscordGIFBot
![version](https://img.shields.io/github/v/tag/JManch/DiscordGIFBot?label=version)

A simple discord bot that stores a database of GIF URLs and posts GIFs when their name is used. Aims to fix the problem of having a long favourite GIF list that is annoying to scroll through.

## Usage

- A list of bot commands can be viewed by typing `gifhelp`
- To mitigate the visual impact of bot messages, I suggest giving the bot an invisible nickname
- The GIF database is stored in the script's directory as `db.json`
- The bot can be used across multiple servers so each server will have their own GIFs
- Although the bot is intended for GIFs it can be used for any media in the form of a URL

## Limitations

When a user sends a message containing the name of a GIF, the posted GIF would ideally be a part of the user's original message in order to avoid a message gap. Unfortunately, the discord API does not allow bots to edit messages or post messages as a user.

To get around this the bot will delete the user's original message and post it again as themselves with the GIF included. The first line of the bot's message will contain the orginal message owner's name in bold. It's not an ideal solution but it's the best I could come up with given the API limitations.

## Self-Hosting

To self-host the bot you must have Python version 3.10 or newer installed.
1. Create and activate a python virtual environment (optional but recommended)
2. Run the command `pip install -r requirements.txt`
3. Create a file called .env and add `TOKEN=INSERT_BOT_TOKEN_HERE` to the first line
4. Run the bot with `python3 gif_bot.py` or use the linux scripts start.sh and stop.sh to run it in the background
5. Create a bot invite with the following permissions
    - Read Message/View Channels
    - Send Messages
    - Manager Messages
