from discord.ext import commands
import discord
import random
import os
from pymongo import MongoClient
mongo_url = os.environ.get("MONGO_URL")
cluster = MongoClient(mongo_url)
db = cluster["Sentry"]
collection = db["econ"]
class economy(commands.Cog,name="economy"):
    def __init__(self,bot):
          self.bot = bot
    @commands.command(name="Rob",description="Rob a user!")
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def rob(self,ctx,*,member:discord.Member):
        choice = random.randint(0,1)
        user = collection.find_one({"_id":ctx.author.id})
        victim = collection.find_one({"_id":member.id})
        if(collection.count_documents({"_id":ctx.author.id}) == 0):
            await ctx.send(f"{member.name} isn't participating in our economy system yet! If they'd like to, ask them to type `pog bal`")
            return
        else:
            if victim['wallet'] > user['wallet']:
                high = user['wallet']
            elif victim['wallet'] < user['wallet']:
                high = victim['wallet']
            else:
                high = user['wallet']
            high = int(high)
            amt = random.randint(0,high)
            if choice == 1:
                wamt = (amt - (amt * 2))
                collection.update_one({"_id":ctx.author.id},{'$inc':{'wallet':amt}})
                collection.update_one({"_id":member.id},{'$inc':{'wallet':wamt}})
                await ctx.send(f"**{ctx.author.name}** just stole **{amt}** pog coins from **{member.name}**!")
            else:
                wamt = (amt - (amt * 2))
                collection.update_one({"_id":ctx.author.id},{'$inc':{'wallet':wamt}})
                await ctx.send(f"**{ctx.author.name}** just tried to rob **{member.name}**, but was caught! They paid a **{amt}** pog coin fine.")

    @commands.command(name="Work",description="Work for some amadola!",usage="work")
    @commands.cooldown(1, 360, commands.BucketType.user)
    async def work(self,ctx):
        jobs = ["exit scammer", "bot dev", "president","Youtuber","pro gamer","pro geimer","stonks invester","stock investor","rapper","chicken nugget","meatball","medical assisstant","doctor","fabio","fake girlfriend","bank robber","decent person","mother (**SUS!**)", "cripto exchangre", "crypto exchanger","Inspiration Ninja","cult leader","dollar","robber(?)","pranker"]
        job = random.choice(jobs)
        money = random.randint(0,3000)
        jobmsg = f"You worked as a **{job}** and earned **{money} pog coins**"
        if(collection.count_documents({"_id":ctx.author.id}) == 0):
            meminfo = {"_id":ctx.author.id,"bank":0,"wallet":0}
            collection.insert_one(meminfo)
        user = collection.find_one({"_id":ctx.author.id})
        collection.update_one({"_id":ctx.author.id},{'$inc':{'wallet':money}})
        await ctx.send(jobmsg)

    @commands.command(aliases=['dep','bank'],name="Deposit",description="Deposit some money into your bank account!",usage="deposit <money>")
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def dep(self,ctx,amt=0):
        if amt == 0:
            await ctx.send("You forgot to tell me how much money you wanted to deposit!")
        try:
            amt = int(amt)
        except ValueError:
            await ctx.send("You didn't give me a number! How was I supposed to work with that?")
        if(collection.count_documents({"_id":ctx.author.id}) == 0):
            meminfo = {"_id":ctx.author.id,"bank":0,"wallet":0}
            collection.insert_one(meminfo)
        user = collection.find_one({"_id":ctx.author.id})
        if (user['wallet']) < amt:
            await ctx.send("You don't have enough money in your wallet for that!")
        else:
            wamt = (amt - (amt * 2))
            collection.update_one({"_id":ctx.author.id},{'$inc':{'wallet':wamt}})
            collection.update_one({"_id":ctx.author.id},{'$inc':{'bank':amt}})
            await ctx.send(f"You just deposited **{amt}** pog coins into your bank account!")

    @commands.command(name="Withdraw",description="Withdraw pog coins from your bank account!",usage="withdraw <number>",aliases=['with'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def withdraw(self,ctx,amt=0):
        if amt == 0:
            await ctx.send("You forgot to tell me how much money you wanted to deposit!")
        try:
            amt = int(amt)
        except ValueError:
            await ctx.send("You didn't give me a number! How was I supposed to work with that?")
        if(collection.count_documents({"_id":ctx.author.id}) == 0):
            meminfo = {"_id":ctx.author.id,"bank":0,"wallet":0}
            collection.insert_one(meminfo)
        user = collection.find_one({"_id":ctx.author.id})
        if (user['bank']) < amt:
            await ctx.send("You don't have enough money in the bank for that!")
        else:
            wamt = (amt - (amt * 2))
            collection.update_one({"_id":ctx.author.id},{'$inc':{'wallet':amt}})
            collection.update_one({"_id":ctx.author.id},{'$inc':{'bank':wamt}})
            await ctx.send(f"You just withdrew **{amt}** pog coins from your bank account!")

    @commands.command(name="Beg",description="Beg strangers for money!",usage="beg")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def beg(self,ctx):
        c = random.randint(0,1)
        people = ["Joe Mama","Johnathan McReynolds","Leonardo DiCaprio","Your mom","PewDiePie","Tiko","peepo","pepe"]
        messages= ['you stanky', 'no u lmao',"what you don't have a job?","I don't speak poor"]
        donor = random.choice(people)
        if c == 1:
            guild = ctx.guild
            guild = guild.id
            ginfo = {"_id": ctx.author.id}
            if(collection.count_documents(ginfo) == 0):
                meminfo = {"_id":ctx.author.id,"bank":0,"wallet":0}
                collection.insert_one(meminfo)
            money = random.randint(34,120)
            msg = f"**{donor}** gave {money} pog coins to {ctx.author.name}!"
            user = collection.find_one({"_id":ctx.author.id})
            collection.update_one({"_id":ctx.author.id},{'$inc':{'wallet':money}})
            await ctx.send(msg)
        else:
            m = random.choice(messages)
            await ctx.send(f"{donor}: {m}")

    @commands.command(name="Balance",description="Check your balance!",usage="balance [user]",aliases=['bal','money','cash'])
    async def balance(self,ctx,member:discord.Member=0):
        if member == 0:
            member = ctx.author
        ginfo = {"_id": member.id}
        if(collection.count_documents(ginfo) == 0):
            meminfo = {"_id":member.id,"bank":0,"wallet":0}
            collection.insert_one(meminfo)
        user = collection.find_one({"_id":member.id})
        walletamt = user["wallet"]
        bankamt = user["bank"]
        embed = discord.Embed(title=f"{member.name}'s balance",color=ctx.author.color)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Wallet",value=f"{walletamt} pog coins")
        embed.add_field(name="Bank",value=f"{bankamt} pog coins")
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(economy(bot))
