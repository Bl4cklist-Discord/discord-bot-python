import html
import random

import discord
import feedparser
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext import commands


class RSSFeeds(commands.Cog):

    def __init__(self, client):
        self.bot = client

        scheduler = AsyncIOScheduler()

        # aufgabe jeden tag um X zeit
        scheduler.add_job(self.news_feed, CronTrigger(hour="20", minute="42", second="0"))

        scheduler.start()

    async def news_feed(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(1188198205180084285)
        rssfeed = feedparser.parse("https://www.gamestar.de/rss/gamestar.rss")
        newest_article = rssfeed.entries[0]

        description = str(newest_article.summary).split("</a>")[1]
        description = html.unescape(description)

        embed = discord.Embed(title="Neue Gaming-News!", color=discord.Color.random(),
                              description=f"**[{newest_article.title}]({newest_article.link})**\n\n"
                                          f"> _{description}_")
        embed.set_footer(text="News von GameStar.de")
        embed.set_image(url=str(newest_article.media_content[0]['url']))

        await channel.send(embed=embed)


async def setup(client):
    await client.add_cog(RSSFeeds(client))
