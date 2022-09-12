import os
import typing
import asyncio
import logging

import discord
from discord.ext import commands
from discord import app_commands

GUILD_ID = 1234 #Your discord guild ID here

class DiscordBot(commands.Bot):

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents, case_insensitive=True)

    
    async def setup_hook(self) -> None:
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")

    async def on_ready(self):
        print(f"Bot is online - {self.user.name}")



bot = DiscordBot()



def is_authorised(ctx):
    return int(ctx.author.id) == 1234 #TODO Your discord user ID here



@bot.hybrid_command(name="logout", with_app_command=True, description='Shuts down the bot.')
@app_commands.guilds(discord.Object(id=GUILD_ID))
@commands.check(is_authorised)
async def off(ctx: commands.Context):
    await ctx.send(f"Shutting down... [{str(ctx.author)}]")
    print(f"Bot shutting down... [{str(ctx.author)}]")
    logger.info(f"Bot shutting down... [{str(ctx.author)}]")
    await bot.close()

@bot.hybrid_command(name="load", with_app_command=True, description='Loads a cogs')
@app_commands.guilds(discord.Object(id=GUILD_ID))
@commands.check(is_authorised)
async def load(ctx: commands.Context , extension: str):
    try:
        await bot.load_extension(f'cogs.{extension}')
        logger.info(f"Loaded {extension} [{str(ctx.author)}]")
        await ctx.send(f"Loaded {extension}")
    except:
        await ctx.send(f"Unable to load {extension}")

@bot.hybrid_command(name="unload", with_app_command=True, description='Unloads a cogs')
@app_commands.guilds(discord.Object(id=GUILD_ID))
@commands.check(is_authorised)
async def unload(ctx: commands.Context, extension: str):
    try:
        await bot.unload_extension(f'cogs.{extension}')
        logger.info(f"Unloaded {extension} [{str(ctx.author)}]")
        await ctx.send(f"Unloaded {extension}")
    except:
        await ctx.send(f"Unable to unload {extension}")

@bot.hybrid_command(name="reload", with_app_command=True, description='Reloads cogs')
@app_commands.guilds(discord.Object(id=GUILD_ID))
@commands.check(is_authorised)
async def reload(ctx: commands.Context, extension:str):
    await ctx.send("Reloading...")
    await bot.reload_extension(f'cogs.{extension}')
    await ctx.send("Reload complete.")
    logger.info(f"Reloaded {extension} - [{str(ctx.author)}]")

@bot.hybrid_command(name="cogs", with_app_command=True, description='Shows a list of cogs')
@app_commands.guilds(discord.Object(id=GUILD_ID))
@commands.check(is_authorised)
async def show_cogs(ctx: commands.Context):
    cogs = [f"`{filename[:-3]}`" for filename in os.listdir(f'./cogs') if filename.endswith('.py')]
    desc = "\n".join(cogs)
    embed = discord.Embed(title="Cogs", description=desc , color=0x3498db)
    await ctx.send(embed=embed)


# Works like:
# .sync -> global sync
# .sync ~ -> sync current guild
# .sync * -> copies all global app commands to current guild and syncs
# .sync ^ -> clears all commands from the current guild target and syncs (removes guild commands)
# .sync id_1 id_2 -> syncs guilds with id 1 and 2

@bot.command()
@commands.guild_only()
@commands.check(is_authorised)
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: typing.Optional[typing.Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

    logger.info(f"Synced {spec} | {guilds} - [{str(ctx.author)}]")


## Setup logging
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

handler = logging.FileHandler(
    filename='logs/discord.log',
    encoding='utf-8'
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)


async def main():
    async with bot:
        await bot.start("Token")


if __name__ == "__main__":
    done = asyncio.run(main())