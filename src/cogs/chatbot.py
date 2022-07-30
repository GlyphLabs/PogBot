from discord.ext import commands
from discord import Guild, TextChannel, Message
from random import choice
from os import environ
from aiohttp import ClientSession
from typing import Optional
from db import GuildSettings
from bot import PogBot
from discord.ext.bridge.core import bridge_command

# initiate the object

dunno = (  # List of error responses for ai
    "IDK.",
    "I don't really know.",
    "Could you rephrase that?",
    "Come again?",
    "Say that again?",
    "Huh?",
    "What?",
)


class chatbot(commands.Cog):
    def __init__(self, client: PogBot):
        self.client = client
        self.cd_mapping = commands.CooldownMapping.from_cooldown(
            4, 10, commands.BucketType.member
        )
        self.bid = environ.get("BRAINSHOP_ID")
        self.bkey = environ.get("BRAINSHOP_KEY")
        self.http = ClientSession()

    def cog_unload(self):
        self.client.loop.create_task(self.http.close())

    @bridge_command()
    async def aichannel(self, ctx: commands.Context, channel: TextChannel):
        await GuildSettings.update_chatbot_channel(ctx.guild.id, channel.id)
        await ctx.send("Set AI channel to " + channel.name)
        await channel.send("Hi I am Pog Memer, you can chat with me here")

    async def get_ai_channel(self, guild: Guild) -> Optional[int]:
        d = await GuildSettings.get(guild.id)
        if d:
            return d.chatbot_channel
        return None

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if (
            message.author.id == self.client.user.id
            or not message.guild
            or message.channel.id != (c := await self.get_ai_channel(message.guild))
        ):
            return
        channel = message.channel
        bucket = self.cd_mapping.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            return await channel.send("Woah, slow down!")
        try:
            await channel.trigger_typing()
            response = await self.http.get(
                f"http://api.brainshop.ai/get?bid={self.bid}&key={self.bkey}&uid={message.author.id}&msg={message.content}"
            )
            res = await response.json()
            await message.reply(res["cnt"])
        except:
            await message.reply(choice(dunno))  # # nosec: B311

    @bridge_command()
    async def ai(self, ctx: commands.Context, message: Message):
        bucket = self.cd_mapping.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            return await ctx.send("Woah, slow down!")
        try:
            response = await self.http.get(
                f"http://api.brainshop.ai/get?bid={self.bid}&key={self.bkey}&uid={message.author.id}&msg={message.content}"
            )
            res = await response.json()
            await message.reply(res["cnt"])
        except:
            await message.reply(choice(dunno))  # nosec: B311


def setup(client):
    client.add_cog(chatbot(client))
