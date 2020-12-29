from twitchio.ext import commands
import twitchio

import os

import dotenv

dotenv.load_dotenv()


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            irc_token=os.environ.get("TOKEN"),
            client_id=os.environ.get("client_id"),
            nick="DoobMe",
            prefix="!",
            initial_channels=["mmattbtw", "DoobMe", "C3AGLE"],
        )

    async def event_ready(self):
        print(f"Ready | {self.nick}")

    async def event_message(self, message):
        print("[MESSAGE LOGS] " + message.author.name + " - " + message.content)
        await self.handle_commands(message)

    @commands.command(name="ping")
    async def test_command(self, ctx):
        await ctx.send(f"FeelsDankMan 🔔 ding @{ctx.author.name}")


bot = Bot()
bot.run()

# mmattbtw uid - 47981391
