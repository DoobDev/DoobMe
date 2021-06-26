import datetime
from aiohttp import request
import twitchio
from twitchio.ext import commands

import os

import dotenv

import json

with open("config.json") as config_file:
    config = json.load(config_file)

dotenv.load_dotenv()


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            irc_token=os.environ.get("TOKEN"),
            client_id=os.environ.get("client_id"),
            nick=config["nickname"],
            prefix=config["prefix"],
            initial_channels=config["channels"],
        )

    async def event_ready(self):
        print(f"Ready | {self.nick}")

    async def event_message(self, message):
        print(
            f"[MESSAGE LOGS] ({message.channel.name}) "
            + message.author.name
            + " - "
            + message.content
        )
        await self.handle_commands(message)

    @commands.command(name="ping", aliases=["ding"])
    async def test_command(self, ctx):
        await ctx.send(f"FeelsDankMan 🔔 ding @{ctx.author.name}")

    @commands.command(name="commands", aliases=["help"])
    async def help_command(self, ctx):
        await ctx.send(
            f"{ctx.author.name}, You can find all of the commands here FeelsGoodMan 👉 https://mmatt.gitbook.io/doobme/doobme-commands"
        )

    @commands.command(name="spam")
    async def spam_command(self, ctx, time: int, *, message: str):
        if "moderator" or "broadcaster" in ctx.author.badges:
            for i in range(0, time):
                await ctx.send(message)
                print(time)
        else:
            await ctx.send("MODS only LUL")

    @commands.command(name="lastfm", aliases=["fm"])
    async def lastfm_command(self, ctx, username: str):

        User_URL = f"https://ws.audioscrobbler.com/2.0/?method=user.getinfo&user={username}&api_key={os.environ.get('lastfmkey')}&format=json"
        top_tracks_url = f"https://ws.audioscrobbler.com/2.0/?method=user.gettoptags&user={username}&api_key={os.environ.get('lastfmkey')}&limit=5&format=json"
        loved_tracks_url = f"https://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user={username}&api_key={os.environ.get('lastfmkey')}&format=json"
        recent_tracks_url = f"https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={username}&api_key={os.environ.get('lastfmkey')}&format=json&limit=1"

        async with request("GET", User_URL) as response:
            if response.status == 200:
                data = (await response.json())["user"]

                title=f"{data['name']}'s Last.fm profile"
                url=data["url"]

                ts = int(data["registered"]["unixtime"])

                playcount = f"{data['playcount']}"
                
                country = data["country"]
                
                #registered_time = datetime.utcfromtimestamp(ts).strftime("%m-%d-%Y | %H:%M:%S")

                async with request("GET", loved_tracks_url) as loved:
                    loved_data = (await loved.json())["lovedtracks"]["@attr"]

                    loved_tracks_total = loved_data["total"]

                async with request("GET", top_tracks_url) as tags:
                    tags_data = (await tags.json())["toptags"]

                    tags_list = list()

                    for i in tags_data["tag"]:
                        tags_list.append(i["name"])

                        top_tags = ", ".join(tags_list)

                async with request("GET", recent_tracks_url) as recent:
                    recent_data = (await recent.json())["recenttracks"]

                    most_recent_track = f"{recent_data['track'][0]['artist']['#text']} - {recent_data['track'][0]['name']}"

                if data["type"] == "subscriber":
                    lastfm_pro_status = "Subscribed"

                await ctx.send(f"{title}: {url} . Play Count: {playcount}, Country: {country}, Loved Tracks: {loved_tracks_total}, Most Recent Track: {most_recent_track}")

            else:
                await ctx.send(f"The Last.fm API returned a {response.status} status.")


bot = Bot()
bot.run()
