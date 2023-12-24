import discord
from discord.ext import commands
import asyncio

class ThreadCreate(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        if thread.parent.id == 1188491894741811241: # Füge hier die ID des Forum-Kanals ein (Rechtsklick auf den Kanal, danach ganz unten ID kopieren)
            embed = discord.Embed(
            description="Vielen Dank, dass du dich gemeldet hast. Wir schätzen dies sehr.",
            color=discord.Color.random(),
            )
            await asyncio.sleep(3) # Verzögerung von 3 Sekunden beim Senden
            await thread.send(embed=embed)


async def setup(client):
    await client.add_cog(ThreadCreate(client))

