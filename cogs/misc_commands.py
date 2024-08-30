import discord
from discord import app_commands, Interaction, Embed
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

    @app_commands.command(name="leaderboard", description="Schau dir die User an, die am längsten aufm Server sind")
    @app_commands.guild_only()
    async def leaderboard_cmd(self, interaction: Interaction):
        # Auf Slash COmmand reagieren, da Discord nur 3 Sekunden Zeit gibt
        await interaction.response.defer(thinking=True, ephemeral=True)

        # Bestenliste für die Uaser, die am längsten aufm server sind
        member_list = sorted([(m.joined_at, m.mention) for m in interaction.guild.members], key=lambda x: x[0])

        # formattierung fürs embed
        desc = ""
        position = 1
        for join_date, user in member_list:
            position_emoji = f"{position}"

            if position == 1:
                position_emoji = ":trophy:"
            elif position == 2:
                position_emoji = ":second_place:"
            elif position == 3:
                position_emoji = ":third_place:"

            desc += f"**{position_emoji}** {user} - <t:{str(join_date.timestamp()).split('.')[0]}:f>\n"
            position += 1

        embed = Embed(title="Top #10 Bestenliste (Mitgliedschaft)", description=desc)
        await interaction.followup.send(embed=embed)






















async def setup(client):
    await client.add_cog(MiscCommands(client))
