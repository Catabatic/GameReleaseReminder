import os
import time
import requests
import json

import discord
from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv
from igdb.wrapper import IGDBWrapper

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
CHANNEL = int(os.getenv("DISCORD_CHANNEL"))
TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")

r = requests.post(f"https://id.twitch.tv/oauth2/token?client_id={TWITCH_CLIENT_ID}&client_secret={TWITCH_CLIENT_SECRET}&grant_type=client_credentials")
access_token = json.loads(r._content)['access_token']

wrapper = IGDBWrapper(TWITCH_CLIENT_ID, access_token)

bot = commands.Bot(command_prefix='/')

@bot.command()
async def remindme(ctx, arg):

    search = ctx.message.content[10:]
    byte_array = wrapper.api_request(
            'games',
            f'search "{search}"; fields id, name, first_release_date;'
        )

    s = byte_array.decode("utf-8")
    data = json.loads(s)
    game = data[0]
    await ctx.send(f'{game["name"]} will be released on: {datetime.utcfromtimestamp(game["first_release_date"]).strftime("%Y-%m-%d")}')
    print(data);

bot.run(TOKEN)