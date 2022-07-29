from discord.ext import commands, tasks
import aiohttp
import discord
from cachetools import TTLCache
from random import choice
from asyncio import sleep
from collections import deque
from typing import Deque
from ormsgpack import packb, unpackb


class Meme(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.memehistory: TTLCache[str, Deque[bytes]] = TTLCache(100, 3600)
        self.memecache: TTLCache[str, Deque[bytes]] = TTLCache(100, 3600)
        self.allmemes: Deque[bytes] = deque()
        self.get_more_memes.start()

    def remove_duplicates(self, l: list):
        final_list = []
        for i in l:
            if i not in final_list:
                final_list.append(i)
        return final_list

    @commands.command(
        name="Meme",
        description="Returns a random meme!",
        aliases=["memz"],
        usage="meme",
    )
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.guild_only()
    async def meme(self, ctx, sub: str = None):
        if not self.memecache:
            await ctx.trigger_typing()
        else:
            memej: dict = unpackb(choice(self.allmemes))
        if sub:
            if sub in self.memecache and self.memecache[sub]:
                memej = choice(unpackb(self.memecache[sub]))
            else:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"https://meme-api.herokuapp.com/gimme/{sub}/50"
                    ) as memedata:
                        memed = await memedata.json()
                        if memedata.status != 200:
                            return await ctx.send("Invalid Sub!")
                        memej = choice(memed["memes"])
                        self.memecache[sub] = deque()
                        self.memecache[sub]
                        
        caption = memej["title"]
        memeurl = memej["url"]
        sub = f"r/{memej['subreddit']}"
        link = memej["postLink"]
        ups = memej["ups"]
        author = memej["author"]
        embed = discord.Embed(
            title=caption, description=f"[Post]({link})", color=ctx.author.color
        )
        embed.set_author(name=f"{sub}", url=f"https://reddit.com/{sub}")
        embed.set_footer(text=f"👍 {ups} • u/{author}")
        embed.set_image(url=memeurl)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def showerthought(self, ctx):
        if ctx.guild.id not in self.memecache:
            self.memecache[ctx.guild.id] = []
        if not self.bot.showercache:
            await ctx.trigger_typing()
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://www.reddit.com/r/showerthoughts/top.json?limit=100"
                ) as response:
                    self.bot.showercache = await response.json()

        attempts = 1
        while attempts < 5:
            if "error" in self.bot.showercache:
                print("failed request {}".format(attempts))
                await sleep(2)
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        "https://www.reddit.com/r/showerthoughts/top.json?limit=100"
                    ) as response:
                        self.bot.showercache = await response.json()
                attempts += 1
            else:
                items = self.bot.showercache["data"]["children"]
                random.shuffle(items)
                for index, val in enumerate(items):
                    if "title" in val["data"]:
                        url = val["data"]["title"]
                        accepted = False
                        if url == "What Is A Showerthought?":
                            accepted = False
                        elif url == "Showerthoughts is looking for new moderators!":
                            accepted = False
                        else:
                            accepted = True
                        if accepted:
                            d = {
                                "title": url,
                                "author": val["data"]["author"],
                                "upvotes": val["data"]["ups"],
                                "comments": val["data"]["num_comments"],
                                "url": val["data"]["url"],
                            }
                            if d not in self.memecache[ctx.guild.id]:
                                self.memecache[ctx.guild.id].append(d)
                                if len(self.memecache[ctx.guild.id]) > 63:
                                    self.memecache[ctx.guild.id].pop(
                                        len(self.memecache[ctx.guild.id] - 1)
                                    )

                                break
                st = self.memecache[ctx.guild.id][len(self.memecache[ctx.guild.id]) - 1]
                embed = discord.Embed(
                    description=str(st["title"]), color=discord.Color.random()
                )
                embed.set_author(
                    name="r/showerthoughts", url="https://reddit.com/r/showerthoughts"
                )
                embed.set_footer(text=f"👍 {st['upvotes']} • u/{st['author']}")
                await ctx.send(embed=embed)
                return
            await ctx.send(
                f"_`{str(self.bot.showercache['message'])}` ({str(self.bot.showercache['error'])})_"
            )
            self.bot.showercache = []

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def dankmemes(self, ctx):
        await self.meme(ctx, "dankmemes")

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def antimeme(self, ctx):
        await self.meme(ctx, "antimeme")

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def me_irl(self, ctx):
        await self.meme(ctx, "me_irl")

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def programmerhumor(self, ctx):
        await self.meme(ctx, "ProgrammerHumor")

    @tasks.loop(seconds=30)
    async def get_more_memes(self):
        async with aiohttp.ClientSession() as session:
            d = await session.get("https://meme-api.herokuapp.com/gimme/50")
            data = await d.json()
            memes = [i for i in data["memes"] if not i["nsfw"]]
            for meme in memes:
                if meme["subreddit"] not in self.memecache:
                    self.memecache[meme["subreddit"]] = deque(maxlen=100)
                self.memecache[meme["subreddit"]].appendleft(packb({
                    "title": meme["title"],
                    "author": meme["author"],
                    "subreddit": meme["subreddit"],
                    "postLlink": meme["postLink"],
                    "ups": meme["ups"],
                    "url": meme["url"],
                }))
            self.allmemes = self.remove_duplicates([i for i in self.allmemes] + memes)

    @tasks.loop(hours=24)
    async def reload_memes(self):
        self.memecache.clear()
        self.memecache = []
        await self.get_more_memes()
        print("Reloaded Meme Cache")


def setup(bot):
    bot.add_cog(Meme(bot))
