import discord
from discord import app_commands, Interaction
from discord.ext import commands


class ModalComponent(commands.Cog):

    def __init__(self, client):
        self.client = client

    @app_commands.command(name="bewerben", description="Hier kann man sich bewerben!")
    async def bewerben_cmd(self, interaction: discord.Interaction):
        modal = ApplyModal(title="🚓 - BEWERBEN ALS TEAMLER")
        await interaction.response.send_modal(modal)

# DISCORD KLASSEN

class ApplyModal(discord.ui.Modal):

    one = discord.ui.TextInput(label="WIE HEISST DU?", placeholder="Yannic", required=True, min_length=2, max_length=25,
                               style=discord.TextStyle.short)

    two = discord.ui.TextInput(label="Wann hast du Geburtstag?", placeholder="4. August 2000", required=False,
                               min_length=10, max_length=50, style=discord.TextStyle.short)

    three = discord.ui.TextInput(label="Was sind deine Erfahrungen?", placeholder="ich kann echt gut coden!!!!", required=True,
                                 min_length=100, max_length=500, style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        channel = interaction.guild.get_channel(835256740962238496)

        birthday_desc = "Nicht angegeben"
        if len(self.two.value) != 0:
            birthday_desc = self.two.value

        await channel.send(f"Name des Bewerbers: {self.one.value} \n"
                           f"Geburtsdatum: {birthday_desc} \n"
                           f"Erfahrungen: {self.three.value}")

        await interaction.response.send_message('Deine Bewerbung wurde erfolgreich abgeschickt!', ephemeral=True)










async def setup(client):
    await client.add_cog(ModalComponent(client))
