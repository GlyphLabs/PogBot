import discord
from discord.ext import commands, tasks
import os
import datetime
import time
import asyncio
import random
from discord.ext.commands import clean_content
from cachetools import LRUCache
import aiohttp
import operator
import requests
import json
from asyncio import sleep

devs = [
    536644802595520534,  # thrizzle.#4258
    819786180597907497,  # griffin#1405
    656021685203501066,  # RyZe#7968
    839514280251359292,  # Random_1s#999
]
poglist = [
    "pog",
    "pogger",
    "poggers",
    "pogg",
    "poger",
    "poggus" "Pog",
    "Pogger",
    "Poggers",
    "Pogg",
    "Poger",
    "Poggus",
]
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("Pog", "Pog ", "pog ", "pog"),
    case_insensitive=True,
    intents=discord.Intents.all(),
    owner_ids=devs,
)

bot.showercache = []

bot.remove_command("help")
acceptableImageFormats = [
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".gifv",
    ".webm",
    ".mp4",
    "imgur.com",
]
memeHistory = LRUCache(100)  # only the most recent memes should be blacklisted
memeSubreddits = [
    "BikiniBottomTwitter",
    "memes",
    "2meirl4meirl",
    "deepfriedmemes",
    "MemeEconomy",
    "me_irl",
    "wholesomememes",
]
start_time = time.time()


async def status():
    while True:
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name=f"you type 'pog' in chat"
            )
        )
        await sleep(60)
        await bot.change_presence(activity=discord.Game(name="on prsaw"))
        await sleep(60)
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening, name="music"
            )
        )
        await sleep(10)  ## take off if you want.


@bot.event
async def on_ready():
    await bot.wait_until_ready()
    print("Bot is ready")
    bot.loop.create_task(status())
    # bot.load_extension("cogs.music")


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)
    for i in [c.name.lower() for c in bot.commands]:
        if message.content.lower() in [f"pog{i}", f"pog {i}"]:
            return
    for word in message.content.lower().split(" "):
        if word in poglist:
            await asyncio.sleep(1)
            custom_emoji = discord.utils.get(bot.emojis, name="POG")
            await message.add_reaction(custom_emoji)
    if message.content == "family":
        await message.channel.send(
            "https://tenor.com/view/i-dont-have-friends-i-have-family-theyre-not-my-friends-theyre-my-family-more-than-friends-gif-16061717"
        )


@bot.command()
async def help(ctx, type=None):
    if type == None:
        embed = discord.Embed(colour=discord.Colour.orange())
        embed.set_author(name="Help")
        embed.add_field(
            name="help general", value="Almost everything in the top.gg description."
        )
        embed.add_field(
            name="help text",
            value="Mess around with text, encode or decode stuff and more",
        )
        embed.add_field(
            name="help fun", value="Fun to use commands made for fun ¯\_(ツ)_/¯"
        )
        embed.add_field(
            name="help reddit", value="Posts stuff from subreddits to your discord chat"
        )
        embed.add_field(
            name="help specrypt",
            value="My own, very lightweight form of encryption (secret language) SpectrixDev made because he was bored ig.",
        )
        embed.add_field(
            name="help game-info",
            value="Shows what the most popular games are in the server and who's playing them",
        )
        embed.add_field(name="help music", value="All of the music commands available")
        await ctx.send(embed=embed)
    elif type == "general":
        embed = discord.Embed(colour=discord.Colour.orange())
        embed.set_author(name="General Help")
        embed.add_field(name="ping", value="Sends the bot's latency", inline=False)
        embed.add_field(
            name="links", value="Invite me to your server! :D", inline=False
        )
        embed.add_field(name="botinfo", value="Sends the bots info", inline=False)
        embed.add_field(name="userinfo", value="Sends a user's info", inline=False)
        embed.add_field(
            name="server-info", value="Sends the server's info", inline=False
        )
        embed.add_field(name="uptime", value="Sends the bot's uptime", inline=False)
        await ctx.author.send(embed=embed)
        await ctx.send("Sent you a list of commands in DMs!")
    elif type == "text":
        embed = discord.Embed(colour=discord.Colour.orange())
        embed.add_field(name="reverse", value="Reverses any text", inline=False)
        embed.add_field(
            name="texttobinary", value="Converts any text to binary", inline=False
        )
        embed.add_field(
            name="binarytotext", value="Converts any binary to text", inline=False
        )
        embed.add_field(
            name="drunkify",
            value="RaNdoMizes youR InPUT's cApS AND LoWErCAsE",
            inline=False,
        )
        embed.add_field(
            name="combine", value="Combines one word with another", inline=False
        )
        await ctx.author.send(embed=embed)
        await ctx.send("Sent you a list of commands in DMs!")
    elif type == "fun":
        embed = discord.Embed(colour=discord.Colour.orange())
        embed.set_author(name="Fun Help")
        embed.add_field(
            name="pog",
            value="Type 'Pog' in chat for the bot to send a pog emoji.",
            inline=False,
        )
        embed.add_field(
            name="buzzdance", value="Sends the meme made by the owner!", inline=False
        )
        embed.add_field(name="ship", value="Test love between two users", inline=False)
        embed.add_field(
            name="gay_scanner",
            value="See how gAeY another user is. Shows my level of maturity too",
            inline=False,
        )
        embed.add_field(
            name="dm",
            value="DM anything to any user even if you arent friends with them! :D",
            inline=False,
        )
        embed.add_field(
            name="roast", value="Let PogBot insult someone or yourself", inline=False
        )
        embed.add_field(
            name="eightball", value="Generic. But mine looks better", inline=False
        )
        await ctx.author.send(embed=embed)
        await ctx.send("Sent you a list of commands in DMs!")
    elif type == "reddit":
        embed = discord.Embed(colour=discord.Colour.orange())
        embed.set_author(name="Meme Help")
        embed.add_field(
            name="meme",
            value="Collects fresh memes from different subreddits",
            inline=False,
        )
        embed.add_field(
            name="showerthought", value="Random and interesting thoughts", inline=False
        )
        embed.add_field(
            name="dankmemes", value="The finest memes on Reddit", inline=False
        )
        embed.add_field(
            name="me_irl",
            value="Fresh memes from only the best subreddit",
            inline=False,
        )
        embed.add_field(
            name="programmerhumor", value="Humor for programmers", inline=False
        )
        await ctx.author.send(embed=embed)
        await ctx.send("Sent you a list of commands in DMs!")
    elif type == "game-info":
        embed = discord.Embed(colour=discord.Colour.orange())
        embed.set_author(name="Game Info Help")
        embed.add_field(
            name="currentgames",
            value="Shows the most popular games in order from your server",
        )
        embed.add_field(
            name="whosplaying",
            value="Check who's playing a specific game in your server",
        )
        await ctx.author.send(embed=embed)
        await ctx.send("Sent you a list of commands in DMs!")
    elif type == "specrypt":
        embed = discord.Embed(colour=discord.Colour.orange())
        embed.set_author(name="Specrypt Help")
        embed.add_field(name="encrypt", value="Encrypts plaintext to specrypt")
        embed.add_field(name="decrypt", value="Decrypts specrypted text into plaintext")
    elif type == "music":
        embed = discord.Embed(colour=discord.Colour.orange())
        embed.set_author(name="Music (Beta)")
        embed.add_field(name="play", value="Play any song!")
        embed.add_field(name="skip", value="Skip to the next song in queue")
        embed.add_field(name="pause", value="Pauses the current playing song")
        embed.add_field(
            name="disconnect", value="Disconnect the bot from the voice channel"
        )
        embed.add_field(name="nowplaying", value="Shows the current song thats playing")
        embed.add_field(name="queue", value="Shows all the songs in queue")
        embed.add_field(name="clear", value="Clears the queue")
     elif type == "economy":
        embed = discord.Embed(colour=discord.Colour.orange())
        embed.set_author(name="Economy")
        embed.add_field(name="balance", value="Shows your balance")
        embed.add_field(name="work", value="Earn coins by working!")
        embed.add_field(name="rob", value="Rob any user.")
        embed.add_field(name="dep", value="Deposit your coins to your bank")
        embed.add_field(name="withdraw", value="Withdraw coins from your bank to your wallet")
        await ctx.author.send(embed=embed)
        await ctx.send("Sent you a list of commands in DMs!")
    else:
        await ctx.send("Unknown Category")


@help.error
async def help_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("Um, your DMs are off so I cant help.")


# @bot.command()
# @commands.guild_only()
# @commands.cooldown(1, 5, commands.BucketType.guild)
# async def meme(ctx):
#       async with ctx.typing(): #loading the meme takes a couple moments, this lets the user know the bot is working on it
#         """Memes from various subreddits (excluding r/me_irl. some don't understand those memes)"""
#         async with aiohttp.ClientSession() as session:
#             async with session.get("https://www.reddit.com/r/{0}/hot.json?limit=100".format(random.choice(memeSubreddits))) as response:
#                 request = await response.json()

#         attempts = 1
#         while attempts < 5:
#             if 'error' in request:
#                 print("failed request {}".format(attempts))
#                 await asyncio.sleep(2)
#                 async with aiohttp.ClientSession() as session:
#                     async with session.get("https://www.reddit.com/r/{0}/hot.json?limit=100".format(random.choice(memeSubreddits))) as response:
#                         request = await response.json()
#                 attempts += 1
#             else:
#                 index = 0

#                 for index, val in enumerate(request['data']['children']):
#                     if 'url' in val['data']:
#                         url = val['data']['url']
#                         urlLower = url.lower()
#                         accepted = False
#                         for j, v, in enumerate(acceptableImageFormats):
#                             if v in urlLower:
#                                 accepted = True
#                         if accepted:
#                             if url not in memeHistory:
#                                 memeHistory.append(url)
#                                 if len(memeHistory) > 63:
#                                     memeHistory.popleft()

#                                 break
#                 await ctx.send(memeHistory[len(memeHistory) - 1])
#                 return
#         await ctx.send("_{}! ({})_".format(str(request['message']), str(request['error'])))


@bot.command()
@commands.guild_only()
async def whosplaying(ctx, *, game):
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
                emote = random.choice(
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

        em = discord.Embed(description=msg, colour=discord.Colour(value=0x36393E))
        em.set_author(name=f"Who's playing {game}? {showing}")
        await ctx.send(embed=em)


@bot.command()
@commands.guild_only()
async def currentgames(ctx):
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

    sorted_list = sorted(freq_list.items(), key=operator.itemgetter(1), reverse=True)

    if not freq_list:
        await ctx.send(
            "```Search results:\nNo users are currently playing any games. Odd...```"
        )
    else:
        # Create display and embed
        msg = ""
        max_games = min(len(sorted_list), 10)

        em = discord.Embed(description=msg, colour=discord.Colour(value=0x36393E))
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


@bot.command()
@commands.guild_only()
async def combine(ctx, name1: clean_content, name2: clean_content):
    name1letters = name1[: round(len(name1) / 2)]
    name2letters = name2[round(len(name2) / 2) :]
    ship = "".join([name1letters, name2letters])
    emb = discord.Embed(color=0x36393E, description=f"{ship}")
    emb.set_author(name=f"{name1} + {name2}")
    await ctx.send(embed=emb)


@bot.command()
@commands.guild_only()
async def ship(ctx, name1: clean_content, name2: clean_content):
    shipnumber = random.randint(0, 100)
    if 0 <= shipnumber <= 10:
        status = "Really low! {}".format(
            random.choice(
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
            random.choice(
                [
                    "Still in the friendzone",
                    "Still in that friendzone ;(",
                    "There's not a lot of love there... ;(",
                ]
            )
        )
    elif 20 < shipnumber <= 30:
        status = "Poor! {}".format(
            random.choice(
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
            random.choice(
                [
                    "There's a bit of love there!",
                    "There is a bit of love there...",
                    "A small bit of love is in the air...",
                ]
            )
        )
    elif 40 < shipnumber <= 60:
        status = "Moderate! {}".format(
            random.choice(
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
            random.choice(
                [
                    "I feel the romance progressing!",
                    "There's some love in the air!",
                    "I'm starting to feel some love!",
                ]
            )
        )
    elif 70 < shipnumber <= 80:
        status = "Great! {}".format(
            random.choice(
                [
                    "There is definitely love somewhere!",
                    "I can see the love is there! Somewhere...",
                    "I definitely can see that love is in the air",
                ]
            )
        )
    elif 80 < shipnumber <= 90:
        status = "Over average! {}".format(
            random.choice(
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
            random.choice(
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

    emb = discord.Embed(
        color=shipColor,
        title="Love test for:",
        description="**{0}** and **{1}** {2}".format(
            name1,
            name2,
            random.choice(
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


@bot.command(aliases=["8ball"])
@commands.guild_only()
async def eightball(ctx, *, _ballInput: clean_content):
    """extra generic just the way you like it"""
    choiceType = random.choice(["(Affirmative)", "(Non-committal)", "(Negative)"])
    if choiceType == "(Affirmative)":
        prediction = (
            random.choice(
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

        emb = discord.Embed(
            title="Question: {}".format(_ballInput),
            colour=0x3BE801,
            description=prediction,
        )
    elif choiceType == "(Non-committal)":
        prediction = (
            random.choice(
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
        emb = discord.Embed(
            title="Question: {}".format(_ballInput),
            colour=0xFF6600,
            description=prediction,
        )
    elif choiceType == "(Negative)":
        prediction = (
            random.choice(
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
        emb = discord.Embed(
            title="Question: {}".format(_ballInput),
            colour=0xE80303,
            description=prediction,
        )
    emb.set_author(
        name="Magic 8 ball",
        icon_url="https://www.horoscope.com/images-US/games/game-magic-8-ball-no-text.png",
    )
    await ctx.send(embed=emb)


@bot.command(aliases=["gay"])
@commands.guild_only()
async def gay_scanner(ctx, *, user: discord.Member):
    """very mature command yes haha"""
    if not user:
        user = ctx.author.name
    gayness = random.randint(0, 100)
    if gayness <= 33:
        gayStatus = random.choice(
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
        gayStatus = random.choice(
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
        gayStatus = random.choice(
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
    emb = discord.Embed(description=f"Gayness for **{user}**", color=gayColor)
    emb.add_field(name="Gayness:", value=f"{gayness}% gay")
    emb.add_field(name="Comment:", value=f"{gayStatus} :kiss_mm:")
    emb.set_author(name="Gay-Scanner™")
    await ctx.send(embed=emb)


@bot.command()
@commands.guild_only()
async def ping(ctx):
    msg = await ctx.send("`Pinging bot latency...`")
    times = []
    counter = 0
    embed = discord.Embed(
        title="More information:",
        description="Pinged 4 times and calculated the average.",
        colour=discord.Colour(value=0x36393E),
    )
    for _ in range(3):
        counter += 1
        start = time.perf_counter()
        await msg.edit(content=f"Pinging... {counter}/3")
        end = time.perf_counter()
        speed = round((end - start) * 1000)
        times.append(speed)
        embed.add_field(name=f"Ping {counter}:", value=f"{speed}ms", inline=True)

    embed.set_author(name="Pong!")
    embed.add_field(
        name="Bot latency", value=f"{round(bot.latency * 1000)}ms", inline=True
    )
    embed.add_field(
        name="Average speed",
        value=f"{round((round(sum(times)) + round(bot.latency * 1000))/4)}ms",
    )
    embed.set_footer(text=f"Estimated total time elapsed: {round(sum(times))}ms")
    await msg.edit(
        content=f":ping_pong: **{round((round(sum(times)) + round(bot.latency * 1000))/4)}ms**",
        embed=embed,
    )


@bot.command(aliases=["invite"])
@commands.guild_only()
async def links(ctx):
    embed = discord.Embed(colour=discord.Colour.orange())
    embed.set_author(name="Links")
    embed.add_field(
        name="Support Server",
        value="[Click Here](https://discord.gg/rmjuhraNyD)",
        inline=False,
    )
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


@bot.command()
@commands.guild_only()
async def buzzdance(ctx):
    await ctx.send("https://photos.app.goo.gl/n6w6cYETwCNXuA4w7")


@bot.command()
@commands.guild_only()
async def botinfo(ctx):
    embed = discord.Embed(colour=discord.Colour.orange())
    embed.set_author(
        name="Info",
        icon_url="https://media.discordapp.net/attachments/846429112608620620/846471414076669982/discord-avatar-128-BSK73.gif",
    )
    embed.add_field(name="Owner:", value="Paragonii#6942\nSquook#0001", inline=False)
    embed.add_field(name="Language:", value="Python", inline=False)
    embed.add_field(name="Prefix:", value="pog ", inline=False)
    embed.add_field(name="Bot Created:", value="May 25, 2021", inline=False)
    await ctx.send(embed=embed)


sent_users = []


@bot.command(aliases=["user-info"])
@commands.guild_only()
async def userinfo(ctx, member: discord.Member = None):
    if not member:  # if member is no mentioned
        member = ctx.message.author  # set member as the author
    roles = [role for role in member.roles[1:]]  # don't get @everyone
    embed = discord.Embed(
        colour=discord.Colour.purple(),
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
    print(member.top_role.mention)
    await ctx.send(embed=embed)


@bot.command(aliases=["server-info"])
@commands.guild_only()
async def serverinfo(ctx):
    total_text_channels = len(ctx.guild.text_channels)
    total_voice_channels = len(ctx.guild.voice_channels)
    total_channels = total_text_channels + total_voice_channels

    emb = discord.Embed(
        color=discord.Colour.blue(), timestamp=datetime.datetime.utcnow()
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
    emb.set_thumbnail(url=bot.user.avatar_url)
    await ctx.send(embed=emb)


@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def dm(
    ctx, member: discord.Member, *, content
):  # You missed the other , after the *
    channel = await member.create_dm()
    embed = discord.Embed(colour=discord.Colour.orange())
    embed.set_author(name=f"You got a message from {ctx.author}")
    embed.add_field(name="Message:", value=content, inline=False)
    await channel.send(embed=embed)


@dm.error
async def dm_error(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.send("User not found. Ik its sad.")


@bot.command()
@commands.guild_only()
async def uptime(ctx):
    current_time = time.time()
    difference = int(round(current_time - start_time))
    text = str(datetime.timedelta(seconds=difference))
    embed = discord.Embed(colour=0xC8DC6C)
    embed.add_field(name="Uptime", value=text)
    embed.set_footer(text="Pog Memer")
    try:
        await ctx.send(embed=embed)
    except discord.HTTPException:
        await ctx.send("Current uptime: " + text)


@bot.command()
@commands.guild_only()
async def drunkify(ctx, *, s):
    lst = [str.upper, str.lower]
    newText = await commands.clean_content().convert(
        ctx, "".join(random.choice(lst)(c) for c in s)
    )
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


@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.bot.logout()


@bot.command()
@commands.guild_only()
async def roast(ctx):
    response = requests.get(
        url="https://evilinsult.com/generate_insult.php?lang=en&type=json"
    )
    roast = json.loads(response.text)
    await ctx.send(roast["insult"])


@tasks.loop(hours=1)
async def reload_memecache():
    async with aiohttp.ClientSession() as s:
        d = s.get("https://www.reddit.com/r/showerthoughts/top.json?limit=100")
        bot.showercache = await d.json()
    bot.showercache = []
    bot.memecache = LRUCache(maxsize=1000)


bot.load_extension("cogs.chatbot")
bot.load_extension("jishaku")
bot.load_extension("cogs.error")
bot.load_extension("cogs.meme")
bot.load_extension("cogs.text")
bot.load_extension("cogs.economy")
token = os.environ.get("TOKEN")
bot.run(token)
