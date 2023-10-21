import discord
from discord import app_commands
from discord.ext import commands


class MiscCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @app_commands.command(name="test", description="Dies ist unser erster Slashbefehl!")
    @app_commands.describe(argument1="Bitte gib eine Zahl ein!", argument0="Wähle etwas aus der Liste aus!")
    @app_commands.choices(argument0=[
        app_commands.Choice(name="Auswahl 1", value=1),
        app_commands.Choice(name="Auswahl 2", value=2),
        app_commands.Choice(name="Auswahl 3", value=3)
    ])
    async def test_cmd(self, interaction: discord.Interaction, argument0: app_commands.Choice[int], argument1: int = None):

        if argument1 is None:
            return await interaction.response.send_message("Das `argument1` war optional und wurde gerade nicht angegeben.")

        await interaction.response.send_message(f"Ich habe deinen Befehl erhalten! Deine Zahl lautet {argument1}\n"
                                                f"Deine Auswahl aus der Liste war {argument0.name} (Value: {argument0.value})", ephemeral=True)

async def setup(client):
    await client.add_cog(MiscCommands(client))
