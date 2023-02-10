from discord.ext.commands import Cog, cooldown, BucketType  # type: ignore
from aiohttp import ClientSession
import discord

from bot import PogBot
from discord.ext.commands import slash_command
from discord import ApplicationContext


class Meme(Cog):
    def __init__(self, bot: PogBot):
        self.bot = bot
        self.subreddits = (
            "memes",
            "dankmemes",
            "me_irl",
            "funny",
            "wholesomememes",
            "antimeme",
        )

    @slash_command(
        name="meme",
        description="Returns a random meme from reddit!",
        aliases=["memz"],
        usage="meme [subreddit]",
    )
    @cooldown(1, 2, BucketType.guild)
    async def meme(self, ctx: ApplicationContext, sub: str = None):
        await ctx.defer()
        async with ClientSession() as session:
            res = await session.get(f"https://dreme.hop.sh/{sub if sub else ''}")
        if not res.ok:
            return
        meme: dict = (await res.json())[0]
        embed = discord.Embed(title=meme["title"], color=ctx.author.color)
        embed.set_author(
            name=f"r/{meme['subreddit']}", url=f'https://reddit.com{meme["permalink"]}'
        )
        embed.set_footer(text=f"👍 {meme['ups']} • u/{meme['author']}")
        embed.set_image(url=meme["url"])
        await ctx.respond(embed=embed)

    @slash_command(
        description="Returns a random showerthought from reddit!", usage="showerthought"
    )
    @cooldown(1, 2, BucketType.user)
    async def showerthought(self, ctx):
        await self.meme(ctx, "showerthoughts")

    @slash_command()
    @cooldown(1, 2, BucketType.user)
    async def dankmeme(self, ctx):
        await self.meme(ctx, "dankmemes")

    @slash_command()
    @cooldown(1, 2, BucketType.user)
    async def antimeme(self, ctx):
        await self.meme(ctx, "antimeme")

    @slash_command()
    @cooldown(1, 2, BucketType.user)
    async def me_irl(self, ctx):
        await self.meme(ctx, "me_irl")

    @slash_command(aliases=["codememe"])
    @cooldown(1, 2, BucketType.user)
    async def programmerhumor(self, ctx):
        await self.meme(ctx, "ProgrammerHumor")


def setup(bot):
    bot.add_cog(Meme(bot))
