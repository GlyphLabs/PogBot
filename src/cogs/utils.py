from discord.ext.commands.cog import Cog
from discord.ext.commands.core import is_owner, command, Context
from discord.ext.bridge.core import bridge_command
from discord import Embed, Colour, Member, HTTPException
from time import time, perf_counter
from datetime import datetime, timedelta

from bot import PogBot


class Utils(Cog):
    def __init__(self, bot: PogBot):
        self.bot = bot

    @command(name="reload", aliases=["r"])
    @is_owner()
    async def reload(self, ctx: Context, cog: str = None):
        if not cog:
            for i in tuple(self.bot.cogs.keys()):
                if i == "Jishaku":
                    continue
                self.bot.reload_extension(f"{i.lower()}")
            return await ctx.respond("Reloaded all cogs.")
        try:
            self.bot.reload_extension(f"{cog}")
            await ctx.respond(f"Reloaded `cogs.{cog}`")
        except Exception as e:
            await ctx.send(e.__str__())
            if "has not been loaded" in e.__str__():
                self.bot.load_extension(f"{cog.lower()}")
            await ctx.respond(f"Error: {e}")

    @command()
    @is_owner()
    async def shutdown(self, ctx: Context):
        await ctx.bot.close()

    @bridge_command(name="ping", description="Check bot latency")
    async def ping(self, ctx: Context):
        msg = await ctx.respond("`Pinging bot latency...`")
        times = []
        counter = 0
        embed = Embed(
            title="More information:",
            description="Pinged 4 times and calculated the average.",
            colour=Colour(value=0x36393E),
        )
        for _ in range(3):
            counter += 1
            start = perf_counter()
            await msg.edit(content=f"Pinging... {counter}/3")
            end = perf_counter()
            speed = round((end - start) * 1000)
            times.append(speed)
            embed.add_field(name=f"Ping {counter}:", value=f"{speed}ms", inline=True)

        embed.set_author(name="Pong!")
        embed.add_field(
            name="Bot latency", value=f"{round(self.bot.latency * 1000)}ms", inline=True
        )
        embed.add_field(
            name="Average speed",
            value=f"{round((round(sum(times)) + round(self.bot.latency * 1000))/4)}ms",
        )
        embed.set_footer(text=f"Estimated total time elapsed: {round(sum(times))}ms")
        await msg.edit(
            content=f":ping_pong: **{round((round(sum(times)) + round(self.bot.latency * 1000))/4)}ms**",
            embed=embed,
        )
        return

    @bridge_command(
        name="links", description="See important bot links", aliases=["invite"]
    )
    async def links(self, ctx: Context):
        embed = Embed(colour=Colour.orange())
        embed.set_author(name="Links")
        embed.add_field(
            name="Invite Link",
            value="[Click Here](https://discord.com/api/oauth2/authorize?client_id=846899156673101854&permissions=8&scope=bot)",
            inline=False,
        )
        embed.add_field(
            name="YouTube Channel (main)",
            value="[Click Here](https://www.youtube.com/channel/UCJP8DUAgyVjEMnxbac9btmw?sub_confirmation=1)",
            inline=False,
        )
        embed.add_field(
            name="GitHub",
            value="[Click Here](https://github.com/ahino6942/public-PogBot)",
            inline=False,
        )
        await ctx.respond(embed=embed, ephemeral=True)

    @bridge_command()
    async def botinfo(self, ctx: Context):
        embed = Embed(colour=Colour.orange())
        embed.set_author(
            name="Info",
            icon_url=self.bot.user.avatar.url,
        )
        embed.add_field(
            name="Made By:",
            value="""
            [Paragonii#6942](https://github.com/ahino6942)
            Squook#0001
            [thrzl#4258](https://thrzl.xyz)
            RyZe#7968
            """,
            inline=False,
        )
        embed.add_field(name="Language:", value="Python", inline=False)
        embed.add_field(name="Prefix:", value="pog ", inline=False)
        embed.add_field(name="Bot Created:", value="May 25, 2021", inline=False)
        await ctx.respond(embed=embed)

    @bridge_command(
        name="userinfo",
        description="Get information about a certain user!",
        aliases=["user-info"],
    )
    async def userinfo(self, ctx: Context, member: Member = None):
        member = ctx.author if not member else member
        roles = [role for role in member.roles[1:]]  # don't get @everyone
        embed = Embed(
            colour=Colour.purple(),
            timestamp=ctx.message.created_at,
            title=f"User Info - {member}",
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author}")

        embed.add_field(name="ID:", value=str(member.id))
        embed.add_field(name="Display Name:", value=member.display_name)

        embed.add_field(
            name="Created Account On:",
            value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
        )
        embed.add_field(
            name="Joined Server On:",
            value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
        )

        embed.add_field(name="Roles:", value="".join([role.mention for role in roles]))
        embed.add_field(name="Highest Role:", value=member.top_role.mention)
        await ctx.respond(embed=embed)

    @bridge_command(
        description="Get information about the server!", aliases=["server-info"]
    )
    async def serverinfo(self, ctx: Context):
        total_text_channels = len(ctx.guild.text_channels)
        total_voice_channels = len(ctx.guild.voice_channels)

        emb = Embed(color=Colour.blue(), timestamp=datetime.utcnow())
        emb.set_author(name=f"Server Info - {ctx.guild.name}")

        emb.add_field(name="Server Name:", value=ctx.guild.name, inline=False)
        emb.add_field(name="Server ID:", value=ctx.guild.id, inline=False)
        emb.add_field(name="Owner:", value=ctx.guild.owner, inline=False)
        emb.add_field(name="Region:", value=ctx.guild.region, inline=False)
        emb.add_field(name="Members count:", value=ctx.guild.member_count, inline=False)
        emb.add_field(
            name="Channels count:",
            value=f"{total_text_channels} Text channels\n{total_voice_channels} voice channels",
            inline=False,
        )
        emb.add_field(
            name="Created on:",
            value=ctx.guild.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
        )
        emb.set_footer(text=ctx.author)
        emb.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.respond(embed=emb)

    @bridge_command(description="Check the bot's uptime")
    async def uptime(self, ctx: Context):
        current_time = time()
        difference = int(round(current_time - self.bot.start_time))
        text = str(timedelta(seconds=difference))
        embed = Embed(colour=0xC8DC6C)
        embed.add_field(name="Uptime", value=text)
        embed.set_footer(text="PogBot")
        try:
            await ctx.respond(embed=embed)
        except HTTPException:
            await ctx.respond("Current uptime: " + text)


def setup(bot):
    bot.add_cog(Utils(bot))
