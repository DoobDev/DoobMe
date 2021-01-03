from twitchio.ext import commands
import twitchio

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


bot = Bot()
bot.run()

# mmattbtw uid - 47981391
