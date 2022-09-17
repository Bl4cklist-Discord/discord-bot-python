import discord
from discord.ext import commands
from discord import app_commands

class ExampleContextMenu(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        self.react_message = app_commands.ContextMenu(
            name='React to Message',
            callback=self.react,
        )
        self.bot.tree.add_command(self.react_message)

    async def react(self, interaction: discord.Interaction, message: discord.Message):
        await interaction.response.send_message(content=f'Hey {message.author.mention}, {interaction.user.mention} thinks this is a very cool message!')

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ExampleContextMenu(bot))

