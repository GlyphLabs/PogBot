from discord.ext.commands import cooldown, Context, Cog, BucketType
from discord.ext.commands import slash_command
from discord import Member, Embed
from random import choice, randint
from db import EconomyData
from math import floor


class Economy(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.crime_msgs = (
            "Now for the getaway...",
            "Made out like a bandit!",
            "Smooth criminal...",
        )
        self.jobs = (
            "exit scammer",
            "bot dev",
            "president",
            "Youtuber",
            "pro gamer",
            "pro geimer",
            "stonks invester",
            "stock investor",
            "rapper",
            "chicken nugget",
            "meatball",
            "medical assisstant",
            "doctor",
            "fabio",
            "fake girlfriend",
            "bank robber",
            "decent person",
            "mother (**SUS!**)",
            "cripto exchangre",
            "crypto exchanger",
            "Inspiration Ninja",
            "cult leader",
            "dollar",
            "robber(?)",
            "pranker",
            "A̵̱͇̱͓͓̟͈̼̫͎͓̋̓̀̎̉̐̀̂̇̄H̷̰̼̭͇͍̭͕̥͈̥͆͛̋H̸̨̧̧̧̛͖̟̣͖̙͎̩͔̬̞̽̅͊̄͆̂͛̿͋̌̉̇H̷̜̞͖̮̭̰̠͙͎̖̟͚̜̤͂̕͘͜",
        )

    @slash_command(name="rob", description="Rob a user!")
    @cooldown(1, 120, BucketType.user)
    async def rob(self, ctx: Context, *, member: Member):
        worked = randint(0, 1)
        victim: EconomyData = await EconomyData.get(member.id)
        if victim.wallet == 0:
            return await ctx.reply(
                f"{member.display_name} doesn't have any money in their wallet!"
            )
        thief: EconomyData = await EconomyData.get(ctx.author.id)
        hamt = thief.wallet if thief.wallet > victim.wallet else victim.wallet
        if worked == 1:
            robamt = randint(0, floor(hamt / 3))
            await EconomyData.update_wallet(member.id, victim.wallet - robamt)
            await EconomyData.update_wallet(ctx.author.id, thief.wallet + robamt)
            embed = Embed(
                description=f"You just stole ${robamt} from {member.mention}!"
            )
            embed.set_author(name=choice(self.crime_msgs))
            await ctx.reply(embed=embed)
        else:
            robamt = randint(0, floor(hamt / 4))
            embed = Embed(description=f"The police charge you a {robamt} fine.")
            embed.set_author(name="You were caught!")
            await ctx.reply(embed=embed)

    @slash_command(name="work", description="Work for some amadola!", usage="work")
    @cooldown(1, 360, BucketType.user)
    async def work(self, ctx: Context):
        job = choice(self.jobs)
        money = randint(0, 3000)
        jobmsg = f"You worked as a **{job}** and earned **{money} pog coins**"
        await EconomyData.update_wallet(ctx.author.id, money)
        await ctx.respond(jobmsg)

    @slash_command(
        aliases=["dep", "bank"],
        name="deposit",
        description="Deposit some money into your bank account!",
        usage="deposit <money>",
    )
    @cooldown(1, 10, BucketType.user)
    async def deposit(self, ctx: Context, amt=None):
        if not amt:
            return await ctx.respond(
                "You forgot to tell me how much money you wanted to deposit!"
            )
        try:
            amt = int(amt)
        except ValueError:
            if amt.lower() != "all":
                await ctx.respond(
                    "You didn't give me a number! How was I supposed to work with that?"
                )
        if type(amt) == int and amt < 1:
            return await ctx.respond("😳")
        user = await EconomyData.get(ctx.author.id)
        if type(amt) == str and amt.lower() == "all":
            amt = user.wallet
        if user.wallet < amt:
            await ctx.respond("You don't have enough money in your wallet for that!")
        else:
            await EconomyData.deposit(ctx.author.id, amt)
            await ctx.respond(
                f"You just deposited **{amt}** pog coins to your bank account!"
            )

    @slash_command(
        name="withdraw",
        description="Withdraw pog coins from your bank account!",
        usage="withdraw <number>",
        aliases=["with"],
    )
    @cooldown(1, 10, BucketType.user)
    async def withdraw(self, ctx: Context, amt=None):
        if not amt:
            return await ctx.respond(
                "You forgot to tell me how much money you wanted to withdraw!"
            )
        try:
            amt = int(amt)
        except ValueError:
            if amt.lower() != "all":
                await ctx.respond(
                    "You didn't give me a number! How was I supposed to work with that?"
                )
        if type(amt) == int and amt < 1:
            return await ctx.respond("😳")

        user = await EconomyData.get(ctx.author.id)
        if type(amt) == str and amt.lower() == "all":
            amt = user.bank

        if user.bank < amt:
            await ctx.respond(
                "You don't have enough money in your bank account for that!"
            )
        else:
            await EconomyData.withdraw(ctx.author.id, amt)

            await ctx.respond(
                f"You just withdrew **{amt}** pog coins from your bank account!"
            )

    @slash_command(name="beg", description="Beg strangers for money!", usage="beg")
    @cooldown(1, 30, BucketType.user)
    async def beg(self, ctx: Context):
        c = randint(0, 1)
        people = (
            "Joe Mama",
            "Johnathan McReynolds",
            "Leonardo DiCaprio",
            "Your mom",
            "PewDiePie",
            "Tiko",
            "peepo",
            "pepe",
        )
        messages = (
            "you stanky",
            "no u lmao",
            "what you don't have a job?",
            "I don't speak poor",
        )
        donor = choice(people)
        if c == 1:
            money = randint(34, 120)
            msg = f"**{donor}** gave {money} pog coins to {ctx.author.name}!"
            user = await EconomyData.get(ctx.author.id)
            await EconomyData.update_wallet(ctx.author.id, user.wallet + money)
            await ctx.respond(msg)
        else:
            m = choice(messages)
            await ctx.respond(f"{donor}: {m}")

    @slash_command(
        name="balance",
        description="Check your balance!",
        usage="balance [user]",
        aliases=["bal", "money", "cash"],
    )
    async def balance(self, ctx: Context, member: Member = None):
        await ctx.defer()
        if not member:
            member = ctx.author
        user: EconomyData = await EconomyData.get(member.id)
        embed = Embed(title=f"{member.name}'s balance", color=ctx.author.color)
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="Wallet", value=f"{user.wallet} pog coins")
        embed.add_field(name="Bank", value=f"{user.bank} pog coins")
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Economy(bot))
