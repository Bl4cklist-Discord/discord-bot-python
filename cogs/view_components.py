from typing import Any

import discord
from discord import app_commands, Interaction
from discord._types import ClientT
from discord.ext import commands


class ViewComponents(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.reportmsg_menu = app_commands.ContextMenu(name="Nachricht melden", callback=self.reportmsg_ctx)
        self.client.tree.add_command(self.reportmsg_menu)

    # CONTEXT BEFEHLE

    async def reportmsg_ctx(self, interaction: discord.Interaction, message: discord.Message):
        channel = interaction.guild.get_channel(790957188851040320)
        await channel.send(f'der Nutzer {message.author} wurde gemeldet von {interaction.user} gemeldet!')
        await interaction.response.send_message('Habs abgeschickt, yo')

    # SLASH BEFEHLE

    @app_commands.command(name="button", description="Hier unser Button-Test!")
    async def button_cmd(self, interaction: discord.Interaction):

        view = ConfirmButtons()
        await interaction.response.send_message("Hier ist deine Antwort!", view=view)
        await view.wait()
        if view.value is None:
            return await interaction.edit_original_response(content="Du hast zu lange gebraucht!", view=None)
        elif not view.value:
            return await interaction.edit_original_response(content="Du hast den Vorgang abgebrochen!", view=None)

        await interaction.edit_original_response(content="Aktion erfolgreich!", view=None)

    @app_commands.command(name="dropdown", description="Hier unser Dropdown-Test!")
    @app_commands.choices(kategorie=[
        app_commands.Choice(name="Normales Dropdown", value=1),
        app_commands.Choice(name="Kanal Dropdown", value=2),
        app_commands.Choice(name="Rollen Dropdown", value=3)
    ])
    async def dropdown_cmd(self, interaction: discord.Interaction, kategorie: app_commands.Choice[int]):

        view = DropdownView(kategorie.value)
        await interaction.response.send_message("Hier ist die Bot-Antwort!", view=view, ephemeral=True)





# DISCORD KOMPONENTEN KLASSEN
class ConfirmButtons(discord.ui.View):

    def __init__(self):
        super().__init__()
        self.value = None
        self.timeout = 180

    @discord.ui.button(label="Ja, Aktion durchführen!", style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = True
        self.stop()

    @discord.ui.button(label="Nein, Aktion abbrechen!", style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = False
        self.stop()

class DropdownView(discord.ui.View):
    def __init__(self, kategorie):
        super().__init__()

        if kategorie == 2:
            self.add_item(DropdownChannel())
        elif kategorie == 3:
            self.add_item(DropdownRole())
        else:
            self.add_item(Dropdown())

# DISCORD MODAL ETC.

class Dropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Option 1", description="Beschreibung für Option 1", emoji="🏝️"),
            discord.SelectOption(label="Option 2", description="Beschreibung für Option 2", emoji="🐫"),
            discord.SelectOption(label="Option 3", description="Beschreibung für Option 3", emoji="📐")
        ]

        super().__init__(placeholder="Klicke auf mich!", min_values=1, max_values=2, options=options)

    async def callback(self, interaction: Interaction[ClientT]) -> Any:
        await interaction.response.send_message(f'Du hast {self.values[0]} angeklickt!')

class DropdownRole(discord.ui.RoleSelect):
    def __init__(self):
        super().__init__(placeholder="Wähle eine Rolle aus!", min_values=1, max_values=1)

    async def callback(self, interaction: Interaction[ClientT]) -> Any:
        await interaction.response.send_message(f'Du hast {self.values} angeklickt!')

class DropdownChannel(discord.ui.ChannelSelect):
    def __init__(self):
        super().__init__(placeholder="Wähle einen Kanal aus!", min_values=1, max_values=1)

    async def callback(self, interaction: Interaction[ClientT]) -> Any:
        await interaction.response.send_message(f'Du hast {self.values} angeklickt!')











async def setup(client):
    await client.add_cog(ViewComponents(client))
