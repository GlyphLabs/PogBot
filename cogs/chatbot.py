from discord.ext import commands
import discord
from replit import db
from prsaw import RandomStuffV2
from random import choice
from cachetools import LRUCache

# initiate the object
rs = RandomStuffV2()

dunno = [  # List of error responses for ai
    "IDK.",
    "I don't really know.",
    "Could you rephrase that?",
    "Come again?",
    "Say that again?",
    "Huh?",
    "What?",
]


class chatbot(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.cd_mapping = commands.CooldownMapping.from_cooldown(
            4, 10, commands.BucketType.member
        )
        self.cache = LRUCache(100)

    @commands.command()
    async def aichannel(self, ctx, op, channel: discord.TextChannel):
        db[str(ctx.guild.id)] = str(channel.id)
        await ctx.send("Set ai channel to " + channel.name)
        await channel.send("Hi I am Pog Memer, you can chat with me here")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.client.user.id:
            return
        if not message.guild:
            return
        channel = message.channel
        try:
            db[str(message.guild.id)]
        except:
            return
        if not str(channel.id) == db[str(message.guild.id)]:
            return
        bucket = self.cd_mapping.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            return await channel.send("Woah, slow down!")
        try:
            if message.content.lower() in self.cache:
                return await message.reply(self.cache[message.content.lower()])
            response = rs.get_ai_response(message.content)
            self.cache[message.content.lower()] = response["message"]
            await message.reply(response["message"])
        except:
            await message.reply(choice(dunno))


def setup(client):
    client.add_cog(chatbot(client))
