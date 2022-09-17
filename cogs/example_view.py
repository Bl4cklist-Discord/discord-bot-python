import discord
from discord.ext import commands
from discord import app_commands

import random

class ExampleView(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="food", description="Select your favourite food!")
    @app_commands.guild_only()
    async def food_cmd(self, interaction: discord.Interaction):
        view = DropdownView()

        await interaction.response.send_message(content="What's your favourite food?", view=view)

    @app_commands.command(name="complement", description="Complement someone")
    @app_commands.describe(user="Who to complement")
    @app_commands.guild_only()
    async def complement_cmd(self, interaction: discord.Interaction , user: discord.Member):
        view = ComplementConfirm()

        await interaction.response.send_message(content='Do you want to continue?', view=view)
        # Wait for the View to stop listening for input...
        await view.wait()
        if view.value is None:
            print('Timed out...')
        elif view.value:
            await interaction.channel.send(f"{user.mention} you're awesome!")
        else:
            print('Cancelled...')

    @app_commands.command(name="random", description="Show a message with a button to create random numbers!")
    @app_commands.guild_only()
    async def random_number_cmd(self, interaction: discord.Interaction):
        view = RandomNumberView()
        await interaction.response.send_message(content="Click to create a random number!", view=view)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ExampleView(bot))





class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DropdownComponent())


class DropdownComponent(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label='Pizza', description='Your favourite food is Pizza', emoji='🍕'),
            discord.SelectOption(label='Tacos', description='Your favourite food is Tacos', emoji='🌮'),
            discord.SelectOption(label='Burritos', description='Your favourite food is Burritos', emoji='🌯'),
        ]
        super().__init__(placeholder='Choose your favourite food...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Your favourite food is {self.values[0]}')






class ComplementConfirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Complement Confirmed!', ephemeral=True)
        self.value = True
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Complement Cancelled :(', ephemeral=True)
        self.value = False
        self.stop()



class RandomNumberView(discord.ui.View):

    @discord.ui.button(label='Generate number', style=discord.ButtonStyle.green)
    async def generate(self, interaction: discord.Interaction, button: discord.ui.Button):
        number = random.randint(0,10)

        await interaction.response.send_message(content=f"Your number is {number}!")
