from discord.ext.commands import (  # type: ignore
    Cog,
)
from discord import Embed, Member, Message, ApplicationContext
from random import choice, randint
from aiohttp import ClientSession
from discord.ext.commands import slash_command
from bot import PogBot
from ormsgpack import packb, unpackb
from typing import Dict


class Fun(Cog):
    __slots__ = (
        "bot",
        "snipe_cache"
    )
    def __init__(self, bot: PogBot):
        self.bot = bot
        self.snipe_cache: Dict[int, bytes] = {}

    @Cog.listener()
    async def on_message_delete(self, message: Message):
        if not message.guild:
            return None
        self.snipe_cache[message.guild.id] = packb(
            {"content": message.content, "author": message.author.id}
        )

    @slash_command(description="Get the last deleted message.")
    async def snipe(self, ctx: ApplicationContext):
        msg = unpackb(self.snipe_cache[ctx.guild.id])
        guild = self.bot.get_guild(ctx.interaction.guild_id)
        member = await guild.get_member(msg["author"])
        if not member:
            member = await guild.fetch_member(msg["author"])
        await ctx.send(
            embed=Embed(description=msg["content"]).set_author(
                name=member.display_name, icon_url=member.display_avatar
            )
        )

    @slash_command()
    async def combine(self, ctx: ApplicationContext, name1: str, name2: str):
        name1letters = name1[: round(len(name1) / 2)]
        name2letters = name2[round(len(name2) / 2) :]
        ship = "".join([name1letters, name2letters])
        emb = Embed(color=0x36393E, description=f"{ship}")
        emb.set_author(name=f"{name1} + {name2}")
        await ctx.respond(embed=emb)

    @slash_command()
    async def ship(self, ctx: ApplicationContext, name1: str, name2: str):
        shipnumber = randint(0, 100)
        if 0 <= shipnumber <= 10:
            status = "Really low! {}".format(
                choice(
                    [
                        "Friendzone ;(",
                        'Just "friends"',
                        '"Friends"',
                        "Little to no love ;(",
                        "There's barely any love ;(",
                    ]
                )
            )
        elif 10 < shipnumber <= 20:
            status = "Low! {}".format(
                choice(
                    [
                        "Still in the friendzone",
                        "Still in that friendzone ;(",
                        "There's not a lot of love there... ;(",
                    ]
                )
            )
        elif 20 < shipnumber <= 30:
            status = "Poor! {}".format(
                choice(
                    [
                        "But there's a small sense of romance from one person!",
                        "But there's a small bit of love somewhere",
                        "I sense a small bit of love!",
                        "But someone has a bit of love for someone...",
                    ]
                )
            )
        elif 30 < shipnumber <= 40:
            status = "Fair! {}".format(
                choice(
                    [
                        "There's a bit of love there!",
                        "There is a bit of love there...",
                        "A small bit of love is in the air...",
                    ]
                )
            )
        elif 40 < shipnumber <= 60:
            status = "Moderate! {}".format(
                choice(
                    [
                        "But it's very one-sided OwO",
                        "It appears one sided!",
                        "There's some potential!",
                        "I sense a bit of potential!",
                        "There's a bit of romance going on here!",
                        "I feel like there's some romance progressing!",
                        "The love is getting there...",
                    ]
                )
            )
        elif 60 < shipnumber <= 70:
            status = "Good! {}".format(
                choice(
                    [
                        "I feel the romance progressing!",
                        "There's some love in the air!",
                        "I'm starting to feel some love!",
                    ]
                )
            )
        elif 70 < shipnumber <= 80:
            status = "Great! {}".format(
                choice(
                    [
                        "There is definitely love somewhere!",
                        "I can see the love is there! Somewhere...",
                        "I definitely can see that love is in the air",
                    ]
                )
            )
        elif 80 < shipnumber <= 90:
            status = "Over average! {}".format(
                choice(
                    [
                        "Love is in the air!",
                        "I can definitely feel the love",
                        "I feel the love! There's a sign of a match!",
                        "There's a sign of a match!",
                        "I sense a match!",
                        "A few things can be imporved to make this a match made in heaven!",
                    ]
                )
            )
        elif 90 < shipnumber <= 100:
            status = "True love! {}".format(
                choice(
                    [
                        "It's a match!",
                        "There's a match made in heaven!",
                        "It's definitely a match!",
                        "Love is truely in the air!",
                        "Love is most definitely in the air!",
                    ]
                )
            )

        if shipnumber <= 33:
            shipColor = 0xE80303
        elif 33 < shipnumber < 66:
            shipColor = 0xFF6600
        else:
            shipColor = 0x3BE801

        emb = Embed(
            color=shipColor,
            title="Love test for:",
            description="**{0}** and **{1}** {2}".format(
                name1,
                name2,
                choice(
                    [
                        ":sparkling_heart:",
                        ":heart_decoration:",
                        ":heart_exclamation:",
                        ":heartbeat:",
                        ":heartpulse:",
                        ":hearts:",
                        ":blue_heart:",
                        ":green_heart:",
                        ":purple_heart:",
                        ":revolving_hearts:",
                        ":yellow_heart:",
                        ":two_hearts:",
                    ]
                ),
            ),
        )
        emb.add_field(name="Results:", value=f"{shipnumber}%", inline=True)
        emb.add_field(name="Status:", value=(status), inline=False)
        await ctx.respond(embed=emb)

    @slash_command(description="Determine your future!", aliases=["8ball"])
    async def eightball(self, ctx: ApplicationContext, *, ballInput: str):
        """extra generic just the way you like it"""
        choiceType = randint(1, 3)
        emb = Embed(title=f"Question: {ballInput.capitalize()}", colour=0x3BE801)
        if choiceType == 1:
            prediction = (
                choice(
                    [
                        "It is certain ",
                        "It is decidedly so ",
                        "Without a doubt ",
                        "Yes, definitely ",
                        "You may rely on it ",
                        "As I see it, yes ",
                        "Most likely ",
                        "Outlook good ",
                        "Yes ",
                        "Signs point to yes ",
                    ]
                )
                + ":8ball:"
            )

        elif choiceType == 2:
            prediction = (
                choice(
                    [
                        "Reply hazy, try again ",
                        "Ask again later ",
                        "Better not tell you now ",
                        "Cannot predict now ",
                        "Concentrate and ask again ",
                    ]
                )
                + ":8ball:"
            )
        elif choiceType == 3:
            prediction = (
                choice(
                    [
                        "Don't count on it ",
                        "My reply is no ",
                        "My sources say no ",
                        "Outlook not so good ",
                        "Very doubtful ",
                    ]
                )
                + ":8ball:"
            )
        emb.description = prediction
        emb.set_author(
            name="Magic 8 ball",
            icon_url="https://www.horoscope.com/images-US/games/game-magic-8-ball-no-text.png",
        )
        await ctx.respond(embed=emb)

    @slash_command(name="gay", description="A very mature command...", aliases=["gay"])
    async def gay_scanner(self, ctx: ApplicationContext, *, user: Member):
        """very mature command yes haha"""
        if not user:
            user = ctx.author.name
        gayness = randint(0, 100)
        if gayness <= 33:
            gayStatus = choice(
                [
                    "No homo",
                    "Wearing socks",
                    '"Only sometimes"',
                    "Straight-ish",
                    "No homo bro",
                    "Girl-kisser",
                    "Hella straight",
                ]
            )
            gayColor = 0xFFC0CB
        elif 33 < gayness < 66:
            gayStatus = choice(
                [
                    "Possible homo",
                    "My gay-sensor is picking something up",
                    "I can't tell if the socks are on or off",
                    "Gay-ish",
                    "Looking a bit homo",
                    "lol half  g a y",
                    "safely in between for now",
                ]
            )
            gayColor = 0xFF69B4
        else:
            gayStatus = choice(
                [
                    "LOL YOU GAY XDDD FUNNY",
                    "HOMO ALERT",
                    "MY GAY-SENSOR IS OFF THE CHARTS",
                    "BIG GEAY",
                    "THE SOCKS ARE OFF",
                    "HELLA GAY",
                ]
            )
            gayColor = 0xFF00FF
        emb = Embed(description=f"Gayness for **{user}**", color=gayColor)
        emb.add_field(name="Gayness:", value=f"{gayness}% gay")
        emb.add_field(name="Comment:", value=f"{gayStatus} :kiss_mm:")
        emb.set_author(name="Gay-Scanner™")
        await ctx.respond(embed=emb)

    @slash_command(description="Generate a roast!")
    async def roast(self, ctx: ApplicationContext):
        await ctx.trigger_typing()
        async with ClientSession() as session:
            response = await session.get(
                url="https://evilinsult.com/generate_insult.php?lang=en&type=json"
            )
        roast = await response.json()
        await ctx.respond(roast["insult"])


def setup(bot: PogBot):
    bot.add_cog(Fun(bot))
