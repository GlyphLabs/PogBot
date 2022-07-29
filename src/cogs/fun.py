from discord.ext.commands import Cog, command, guild_only, is_owner, Context, cooldown, BucketType
from operator import itemgetter
from discord import Colour, Embed, Member, HTTPException, MemberNotFound
from random import choice, randint
from time import time, perf_counter
from datetime import datetime, timedelta
from aiohttp import ClientSession

class Fun(Cog):
    def __init_(self, bot): self.bot = bot 

    @command()
    @guild_only()
    async def whosplaying(self, ctx: Context, *, game):
        """Shows who's playing a specific game"""
        if len(game) <= 1:
            await ctx.send(
                "```The game should be at least 2 characters long...```", delete_after=5.0
            )
            return

        guild = ctx.message.guild
        members = guild.members
        playing_game = ""
        count_playing = 0

        for member in members:
            if not member:
                continue
            if not member.activity or not member.activity.name:
                continue
            if member.bot:
                continue
            if game.lower() in member.activity.name.lower():
                count_playing += 1
                if count_playing <= 15:
                    emote = choice(
                        [
                            ":trident:",
                            ":high_brightness:",
                            ":low_brightness:",
                            ":beginner:",
                            ":diamond_shape_with_a_dot_inside:",
                        ]
                    )
                    playing_game += f"{emote} {member.name} ({member.activity.name})\n"

        if playing_game == "":
            await ctx.send(
                "```Search results:\nNo users are currently playing that game.```"
            )
        else:
            msg = playing_game
            if count_playing > 15:
                showing = "(Showing 15/{})".format(count_playing)
            else:
                showing = "({})".format(count_playing)

            em = Embed(description=msg, colour=Colour(value=0x36393E))
            em.set_author(name=f"Who's playing {game}? {showing}")
            await ctx.send(embed=em)


    @command()
    @guild_only()
    async def currentgames(self, ctx: Context):
        """Shows the most played games right now"""
        guild = ctx.message.guild
        members = guild.members

        freq_list = {}
        for member in members:
            if not member:
                continue
            if not member.activity or not member.activity.name:
                continue
            if member.bot:
                continue
            if member.activity.name not in freq_list:
                freq_list[member.activity.name] = 0
            freq_list[member.activity.name] += 1

        sorted_list = sorted(freq_list.items(), key=itemgetter(1), reverse=True)

        if not freq_list:
            await ctx.send(
                "```Search results:\nNo users are currently playing any games. Odd...```"
            )
        else:
            # Create display and embed
            msg = ""
            max_games = min(len(sorted_list), 10)

            em = Embed(description=msg, colour=Colour(value=0x36393E))
            for i in range(max_games):
                game, freq = sorted_list[i]
                if int(freq_list[game]) < 2:
                    amount = "1 person"
                else:
                    amount = f"{int(freq_list[game])} people"
                em.add_field(name=game, value=amount)
            em.set_thumbnail(url=guild.icon_url)
            em.set_footer(
                text="Do pogwhosplaying <game> to see whos playing a specific game"
            )
            em.set_author(name="Top games being played right now in the server:")
            await ctx.send(embed=em)
        return


    @command()
    @guild_only()
    async def combine(self, ctx: Context, name1: str, name2: str):
        name1letters = name1[: round(len(name1) / 2)]
        name2letters = name2[round(len(name2) / 2) :]
        ship = "".join([name1letters, name2letters])
        emb = Embed(color=0x36393E, description=f"{ship}")
        emb.set_author(name=f"{name1} + {name2}")
        await ctx.send(embed=emb)


    @command()
    @guild_only()
    async def ship(self, ctx: Context, name1: str, name2: str):
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
        await ctx.send(embed=emb)


    @command(aliases=["8ball"])
    @guild_only()
    async def eightball(self, ctx: Context, *, _ballInput: str):
        """extra generic just the way you like it"""
        choiceType = choice(["(Affirmative)", "(Non-committal)", "(Negative)"])
        if choiceType == "(Affirmative)":
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

            emb = Embed(
                title="Question: {}".format(_ballInput),
                colour=0x3BE801,
                description=prediction,
            )
        elif choiceType == "(Non-committal)":
            prediction = (
                choice(
                    [
                        "Reply hazy try again ",
                        "Ask again later ",
                        "Better not tell you now ",
                        "Cannot predict now ",
                        "Concentrate and ask again ",
                    ]
                )
                + ":8ball:"
            )
            emb = Embed(
                title="Question: {}".format(_ballInput),
                colour=0xFF6600,
                description=prediction,
            )
        elif choiceType == "(Negative)":
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
            emb = Embed(
                title="Question: {}".format(_ballInput),
                colour=0xE80303,
                description=prediction,
            )
        emb.set_author(
            name="Magic 8 ball",
            icon_url="https://www.horoscope.com/images-US/games/game-magic-8-ball-no-text.png",
        )
        await ctx.send(embed=emb)


    @command(aliases=["gay"])
    @guild_only()
    async def gay_scanner(self, ctx: Context, *, user: Member):
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
                    "STINKY GAY",
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
        await ctx.send(embed=emb)


    @command()
    @guild_only()
    async def ping(self, ctx: Context):
        msg = await ctx.send("`Pinging bot latency...`")
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


    @command(aliases=["invite"])
    @guild_only()
    async def links(self, ctx: Context):
        embed = Embed(colour=Colour.orange())
        embed.set_author(name="Links")
        embed.add_field(
            name="Support Server",
            value="[Click Here](https://gg/rmjuhraNyD)",
            inline=False,
        )
        embed.add_field(
            name="Invite Link",
            value="[Click Here](https://com/api/oauth2/authorize?client_id=846899156673101854&permissions=8&scope=bot)",
            inline=False,
        )
        embed.add_field(
            name="YouTube Channel (main)",
            value="[Click Here](https://www.youtube.com/channel/UCJP8DUAgyVjEMnxbac9btmw?sub_confirmation=1)",
            inline=False,
        )
        embed.add_field(
            name="GitHub",
            value="[Click Here](https://github.com/Paragonii)",
            inline=False,
        )
        embed.add_field(
            name="Changelog",
            value="[Click Here](https://github.com/Paragonii/Bot-Changelogs/blob/main/POGBOT.md)",
            inline=False,
        )
        await ctx.author.send(embed=embed)
        await ctx.send("I sent you them in dms because I dont want to advertise.")


    @command()
    @guild_only()
    async def buzzdance(self, ctx: Context):
        await ctx.send("https://photos.app.goo.gl/n6w6cYETwCNXuA4w7")


    @command()
    @guild_only()
    async def botinfo(self, ctx: Context):
        embed = Embed(colour=Colour.orange())
        embed.set_author(
            name="Info",
            icon_url="https://media.discordapp.net/attachments/846429112608620620/846471414076669982/discord-avatar-128-BSK73.gif",
        )
        embed.add_field(name="Owner:", value="Paragonii#6942\nSquook#0001", inline=False)
        embed.add_field(name="Language:", value="Python", inline=False)
        embed.add_field(name="Prefix:", value="pog ", inline=False)
        embed.add_field(name="Bot Created:", value="May 25, 2021", inline=False)
        await ctx.send(embed=embed)


    @command(aliases=["user-info"])
    @guild_only()
    async def userinfo(self, ctx: Context, member: Member = None):
        if not member:  # if member is no mentioned
            member = ctx.message.author  # set member as the author
        roles = [role for role in member.roles[1:]]  # don't get @everyone
        embed = Embed(
            colour=Colour.purple(),
            timestamp=ctx.message.created_at,
            title=f"User Info - {member}",
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}")

        embed.add_field(name="ID:", value=member.id)
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
        await ctx.send(embed=embed)


    @command(aliases=["server-info"])
    @guild_only()
    async def serverinfo(self, ctx: Context):
        total_text_channels = len(ctx.guild.text_channels)
        total_voice_channels = len(ctx.guild.voice_channels)
        total_channels = total_text_channels + total_voice_channels

        emb = Embed(
            color=Colour.blue(), timestamp=datetime.utcnow()
        )
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
        await ctx.send(embed=emb)


    @command()
    @cooldown(1, 30, BucketType.user)
    async def dm(
        ctx: Context, member: Member, *, content
    ):  # You missed the other , after the *
        channel = await member.create_dm()
        embed = Embed(colour=Colour.orange())
        embed.set_author(name=f"You got a message from {ctx.author}")
        embed.add_field(name="Message:", value=content, inline=False)
        await channel.send(embed=embed)


    @dm.error
    async def dm_error(self, ctx: Context, error):
        if isinstance(error, MemberNotFound):
            await ctx.send("User not found. Ik its sad.")


    @command()
    @guild_only()
    async def uptime(self, ctx: Context):
        current_time = time()
        difference = int(round(current_time - self.bot.start_time))
        text = str(timedelta(seconds=difference))
        embed = Embed(colour=0xC8DC6C)
        embed.add_field(name="Uptime", value=text)
        embed.set_footer(text="Pog Memer")
        try:
            await ctx.send(embed=embed)
        except HTTPException:
            await ctx.send("Current uptime: " + text)


    @command()
    @guild_only()
    async def drunkify(self, ctx: Context, *, s: str):
        lst = (str.upper, str.lower)
        newText = "".join(choice(lst)(c) for c in s)
        if len(newText) <= 380:
            await ctx.send(newText)
        else:
            try:
                await ctx.author.send(newText)
                await ctx.send(
                    f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**"
                )
            except Exception:
                await ctx.send(
                    f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**"
                )


    @command()
    @is_owner()
    async def shutdown(self, ctx: Context):
        await ctx.bot.logout()


    @command()
    @guild_only()
    async def roast(self, ctx: Context):
        await ctx.trigger_typing()
        async with ClientSession() as session:
            response = await session.get(
                url="https://evilinsult.com/generate_insult.php?lang=en&type=json"
            )
        roast = await response.json()
        await ctx.send(roast["insult"])
