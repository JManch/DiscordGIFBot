import os
import logging
from time import perf_counter, sleep

import discord
from dotenv import load_dotenv
from tinydb import TinyDB, Query
from tinydb_smartcache import SmartCacheTable

# Load env vars
load_dotenv()

# Initialise db
TinyDB.table_class = SmartCacheTable
db = TinyDB("db.json")
Gif = Query()

commands = {
    "gifhelp": "`gifhelp` *prints info about available commands*",
    "gifadd": "`gifadd <name> <url>` *saves GIF for current server*",
    "gifremove": "`gifremove <name>` *removes GIF for current server*",
    "giflist": "`giflist [visual]` *visual mode is slow due to discord rate limiting*",
    "gifserverlist": "`gifserverlist` *lists name, ID and GIF count of servers with GIFs saved*",
    "gifserverdelete": "`gifserverdelete <server ID>` *deletes all GIFs for a server, use `gifserverlist` to get ID*",
}


class MyClient(discord.Client):
    async def on_message(self, message):
        # ignore bot messages
        if message.author.id == self.user.id:
            return

        # ignore empty messages
        if not message.content:
            return

        words = message.content.split()
        command = words[0]
        match command:
            case "gifhelp":
                await help(message, words)
                return
            case "gifadd":
                await add(message, words)
                return
            case "gifremove":
                await remove(message, words)
            case "giflist":
                await list(message, words)
                return
            case "gifserverlist":
                await guild_list(self, message, words)
                return
            case "gifserverdelete":
                await guild_delete(message, words)

        await post(message)


# Sends a list of available commands
async def help(message, words):
    if len(words) != 1:
        await message.channel.send("Invalid syntax for `gifhelp` command")
        return
    command_list = "**Commands**"
    for value in commands.values():
        command_list = f"{command_list}\n{value}"
    await message.channel.send(command_list)


# Sends a list of saved GIFs
async def list(message, words):
    # check syntax
    if len(words) > 2 or (len(words) == 2 and words[1] != "visual"):
        await message.channel.send(
            "Invalid syntax for `giflist` command\n" + commands["giflist"]
        )
        return

    visual = len(words) == 2

    gifs = db.search(Gif.guild == message.guild.id)

    if visual:
        await message.channel.send("**Saved GIFs**")
        for gif in gifs:
            await message.channel.send(f"`{gif['name']}`")
            await message.channel.send(f"{gif['url']}")
    else:
        gif_list = "**Saved GIFs**"
        for gif in gifs:
            gif_list = f"{gif_list}\n`{gif['name']}`"
        await message.channel.send(gif_list)


# Lists all servers the bot has saved GIFs for
async def guild_list(client, message, words):
    # check syntax
    if len(words) != 1:
        await message.channel.send("Invalid syntax for `gifserverlist` command")
        return

    guilds = {}
    gif_counts = {}
    all_gifs = db.all()
    for gif in all_gifs:
        guilds[gif["guild"]] = client.get_guild(gif["guild"])
        if gif["guild"] in gif_counts:
            gif_counts[gif["guild"]] += 1
        else:
            gif_counts[gif["guild"]] = 1

    guild_list = "**Servers with Saved GIFS**"
    for id, name in guilds.items():
        guild_list = (
            f"{guild_list}\n*Name* `{name}` *ID* `{id}` *GIF Count* `{gif_counts[id]}`"
        )
    await message.channel.send(guild_list)


# Deletes all GIFs for a server
async def guild_delete(message, words):
    # check syntax
    if len(words) != 2:
        await message.channel.send(
            "Invalid syntax for `gifserverdelete` command\n"
            + commands["gifserverdelete"]
        )

    id = words[1]

    removed_guild = db.remove(Gif.guild == id)
    if not removed_guild:
        await message.channel.send("Server with ID `{id}` does not exist")
    else:
        guild_name = client.get_guild(message.guild.id)
        await message.channel.send(f"Delete all saved GIFs from server with ID `{id}`")


# Saves a GIF
async def add(message, words):
    # check syntax
    if len(words) != 3:
        await message.channel.send(
            "Invalid syntax for `gifadd` command\n" + commands["gifadd"]
        )
        return

    name = words[1]
    url = words[2]

    # check if GIF with name already exists
    existing_gif = db.search((Gif.guild == message.guild.id) & (Gif.name == name))
    if existing_gif:
        db.update(set("url", url), (Gif.guild == message.guild.id) & (Gif.name == name))
        await message.channel.send(
            f"Gif with name `{name}` already exists\nUpdating url from `{existing_gif[0]['url']}` to `{url}`"
        )
    else:
        db.insert({"guild": message.guild.id, "name": name, "url": url})
        await message.channel.send(f"Saved GIF with name `{name}`")


# Removes a GIF
async def remove(message, words):
    # check syntax
    if len(words) != 2:
        await message.channel.send(
            "Invalid syntax for `gifremove` command\n" + commands["gifremove"]
        )
        return

    name = words[1]
    removed_gif = db.remove((Gif.guild == message.guild.id) & (Gif.name == words[1]))
    if not removed_gif:
        await message.channel.send(f"Gif with name `{name}` does not exist")
    else:
        await message.channel.send(f"Removed GIF with name `{name}`")


# Posts a GIF
async def post(message):
    # check if message contains GIF name
    words = message.content.split()
    for i, word in enumerate(words):
        # db search caches queries so this is ok
        gif = db.search((Gif.guild == message.guild.id) & (Gif.name == word))
        if not gif:
            continue
        else:
            # delete the gif name from original message content if used at start or end
            if i == 0 or i == len(words) - 1:
                words[i] = ""
            new_content = " ".join(words)

            # resend original message as bot
            await message.delete()
            # send GIF first if it was first word
            if i == 0:
                await message.channel.send(f"**{message.author.display_name}**")
                await message.channel.send(gif[0]["url"])
                if new_content:
                    await message.channel.send(new_content)
            else:
                await message.channel.send(
                    f"**{message.author.display_name}**\n" + new_content
                )
                await message.channel.send(gif[0]["url"])


intents = discord.Intents.default()
intents.message_content = True

handler = logging.FileHandler(filename="gif_bot.log", encoding="utf-8", mode="w")

client = MyClient(intents=intents)
client.run(os.getenv("TOKEN"), log_handler=handler)
