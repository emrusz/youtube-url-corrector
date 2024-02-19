import os
import re
from contextlib import suppress
from urllib.parse import urlparse, parse_qs

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="?", intents=intents)

PIPED_URL = os.getenv("PIPED_URL") + "/watch?v="
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


@bot.event
async def on_ready():
    print("Ready!")


@bot.event
async def on_message(message):
    regex = re.compile(
        r"https://(music\.)?(www\.)?youtu(be)?\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_+.~#?&/=]*)"
    )

    result = regex.search(message.content)
    if result is not None:
        youtube_url = result.group(0)
        video_id = await get_youtube_id(youtube_url)

        if video_id is not None:
            await message.reply(
                f"I think you meant {PIPED_URL}{video_id}.", mention_author=False
            )


async def get_youtube_id(url: str, ignore_playlist=True) -> str:
    query = urlparse(url)
    if query.hostname == "youtu.be":
        return query.path[1:]
    if query.hostname in {"www.youtube.com", "youtube.com", "music.youtube.com"}:
        if not ignore_playlist:
            # use case: get playlist id not current video in playlist
            with suppress(KeyError):
                return parse_qs(query.query)["list"][0]
        if query.path == "/watch":
            return parse_qs(query.query)["v"][0]
        if query.path[:7] == "/watch/":
            return query.path.split("/")[1]
        if query.path[:7] == "/embed/":
            return query.path.split("/")[2]
        if query.path[:3] == "/v/":
            return query.path.split("/")[2]
        if query.path[:8] == "/shorts/":
            return query.path.split("/")[1]


bot.run(DISCORD_TOKEN)
