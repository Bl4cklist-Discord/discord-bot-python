import asyncio
import os

import discord
from discord.ext import commands

class YouTubeTutorial(commands.Bot):

    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.presences = True
        intents.message_content = True
        super().__init__(command_prefix=".", intents=intents, case_insensitive=True)

    async def setup_hook(self) -> None:

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f"cogs.{filename[:-3]}")

        await self.tree.sync()

    async def on_ready(self):
        print("unser bot sollte jetzt online sein & wir sind bereit!")



bot = YouTubeTutorial()

































































async def discord_login():
    async with bot:
        await bot.start(token="123", reconnect=True)


if __name__ == "__main__":
    done = asyncio.run(discord_login())
