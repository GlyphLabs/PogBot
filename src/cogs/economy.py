from discord.ext.commands import command, cooldown, Context, Cog, BucketType
from discord import Member, Embed
from random import choice, randint
from db import EconomyData
collection = None

class Economy(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.crime_msgs = (
            "Now for the getaway...",
            "Made out like a bandit!",
            "Smooth criminal...",
        )
        self.jobs = jobs = (
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

    @command(name="Rob", description="Rob a user!")
    @cooldown(1, 120, BucketType.user)
    async def rob(self, ctx: Context, *, member: Member):
        worked = randint(0, 1)
        victim: EconomyData = await EconomyData.get(member.id)
        if victim.wallet == 0:
            return await ctx.reply(f"{member.display_name} doesn't have any money in their wallet!")
        thief: EconomyData = await EconomyData.get(ctx.author.id)
        hamt = thief.wallet if thief > victim else victim.wallet
        if worked == 1:
            robamt = randint(0, hamt / 3)
            await EconomyData.update_wallet(member.id, victim.wallet - robamt)
            await EconomyData.update_wallet(ctx.author.id, thief.wallet + robamt)
            embed = Embed(
                description=f"You just stole ${robamt} from {member.mention}!"
            )
            embed.set_author(name=choice(self.crime_msgs))
            await ctx.reply(embed=embed)
        else:
            robamt = randint(0, hamt / 4)
            embed = Embed(description=f"The police charge you a {robamt} fine.")
            embed.set_author(name="You were caught!")
            await ctx.reply(embed=embed)

    @command(name="Work", description="Work for some amadola!", usage="work")
    @cooldown(1, 360, BucketType.user)
    async def work(self, ctx: Context):
        job = choice(self.jobs)
        money = randint(0, 3000)
        jobmsg = f"You worked as a **{job}** and earned **{money} pog coins**"
        EconomyData.update_wallet(ctx.author.id, money)
        await ctx.send(jobmsg)

    @command(
        aliases=["dep", "bank"],
        name="Deposit",
        description="Deposit some money into your bank account!",
        usage="deposit <money>",
    )
    @cooldown(1, 600, BucketType.user)
    async def dep(self, ctx, amt=0):
        if amt == 0:
            await ctx.send(
                "You forgot to tell me how much money you wanted to deposit!"
            )
        try:
            amt = int(amt)
        except ValueError:
            await ctx.send(
                "You didn't give me a number! How was I supposed to work with that?"
            )
        if collection.count_documents({"_id": ctx.author.id}) == 0:
            meminfo = {"_id": ctx.author.id, "bank": 0, "wallet": 0}
            collection.insert_one(meminfo)
        user = collection.find_one({"_id": ctx.author.id})
        if (user["wallet"]) < amt:
            await ctx.send("You don't have enough money in your wallet for that!")
        else:
            wamt = amt - (amt * 2)
            collection.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": wamt}})
            collection.update_one({"_id": ctx.author.id}, {"$inc": {"bank": amt}})
            await ctx.send(
                f"You just deposited **{amt}** pog coins into your bank account!"
            )

    @command(
        name="Withdraw",
        description="Withdraw pog coins from your bank account!",
        usage="withdraw <number>",
        aliases=["with"],
    )
    @cooldown(1, 10, BucketType.user)
    async def withdraw(self, ctx, amt=0):
        if amt == 0:
            await ctx.send(
                "You forgot to tell me how much money you wanted to deposit!"
            )
        try:
            amt = int(amt)
        except ValueError:
            await ctx.send(
                "You didn't give me a number! How was I supposed to work with that?"
            )
        if collection.count_documents({"_id": ctx.author.id}) == 0:
            meminfo = {"_id": ctx.author.id, "bank": 0, "wallet": 0}
            collection.insert_one(meminfo)
        user = collection.find_one({"_id": ctx.author.id})
        if (user["bank"]) < amt:
            await ctx.send("You don't have enough money in the bank for that!")
        else:
            wamt = amt - (amt * 2)
            collection.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": amt}})
            collection.update_one({"_id": ctx.author.id}, {"$inc": {"bank": wamt}})
            await ctx.send(
                f"You just withdrew **{amt}** pog coins from your bank account!"
            )

    @command(name="Beg", description="Beg strangers for money!", usage="beg")
    @cooldown(1, 30, BucketType.user)
    async def beg(self, ctx):
        c = randint(0, 1)
        people = [
            "Joe Mama",
            "Johnathan McReynolds",
            "Leonardo DiCaprio",
            "Your mom",
            "PewDiePie",
            "Tiko",
            "peepo",
            "pepe",
        ]
        messages = [
            "you stanky",
            "no u lmao",
            "what you don't have a job?",
            "I don't speak poor",
        ]
        donor = choice(people)
        if c == 1:
            guild = ctx.guild
            guild = guild.id
            ginfo = {"_id": ctx.author.id}
            if collection.count_documents(ginfo) == 0:
                meminfo = {"_id": ctx.author.id, "bank": 0, "wallet": 0}
                collection.insert_one(meminfo)
            money = randint(34, 120)
            msg = f"**{donor}** gave {money} pog coins to {ctx.author.name}!"
            user = collection.find_one({"_id": ctx.author.id})
            collection.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": money}})
            await ctx.send(msg)
        else:
            m = choice(messages)
            await ctx.send(f"{donor}: {m}")

    @command(
        name="Balance",
        description="Check your balance!",
        usage="balance [user]",
        aliases=["bal", "money", "cash"],
    )
    async def balance(self, ctx: Context, member: Member = None):
        if not member:
            member = ctx.author
        user: EconomyData = await EconomyData.get(member.id)
        embed = Embed(title=f"{member.name}'s balance", color=ctx.author.color)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Wallet", value=f"{user.wallet} pog coins")
        embed.add_field(name="Bank", value=f"{user.bank} pog coins")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Economy(bot))
