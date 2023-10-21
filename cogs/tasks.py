import random

import discord
from discord.ext import commands, tasks


class Tasks(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.status_task.start()

    @tasks.loop(hours=1.0)
    async def status_task(self):
        await self.client.wait_until_ready()

        randomuser = random.choice(self.client.users)
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                    name=str(randomuser),
                                                                    status=discord.Status.idle))



async def setup(client):
    await client.add_cog(Tasks(client))
