import typing

import discord
from discord.ext import commands
from discord import app_commands


class ExampleCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="hello", description="Hi!")
    @app_commands.describe(user="Who to say hello to")
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: i.user.id)
    async def hello_cmd(self, interaction: discord.Interaction, user: typing.Optional[discord.Member] = None):
        if user:
            await interaction.response.send_message(content=f"Hallo {user.mention}!")
        else:
            await interaction.response.send_message(content="Hallo!")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ExampleCog(bot))