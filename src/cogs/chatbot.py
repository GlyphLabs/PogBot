from discord import Guild, TextChannel, Message
from random import choice
from os import environ
from aiohttp import ClientSession
from typing import Optional
from db import GuildSettings
from bot import PogBot
from discord.ext.commands import slash_command, has_permissions, CooldownMapping, BucketType, Cog
from discord import ApplicationContext

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


class Chatbot(Cog):
    def __init__(self, client: PogBot):
        self.client = client
        self.cd_mapping = CooldownMapping.from_cooldown(
            4, 10, BucketType.user
        )
        self.bid = environ.get("BRAINSHOP_ID")
        self.bkey = environ.get("BRAINSHOP_KEY")
        self.http = ClientSession()

    def cog_unload(self):
        self.client.loop.create_task(self.http.close())

    @slash_command(description="Change the AI channel.")
    @has_permissions(manage_channels=True)
    async def aichannel(self, ctx: ApplicationContext, channel: TextChannel):
        await GuildSettings.update_chatbot_channel(ctx.guild.id, channel.id)
        await ctx.respond("Set AI channel to " + channel.name)
        await channel.send("👋🏽 Hi, I'm PogBot! You can chat with me in this channel :)")

    async def get_ai_channel(self, guild: Guild) -> Optional[int]:
        d = await GuildSettings.get(guild.id)
        if d:
            return d.chatbot_channel
        return None

    @Cog.listener()
    async def on_message(self, message: Message):
        if (
            message.author.id == self.client.user.id
            or not message.guild
            or message.channel.id != await self.get_ai_channel(message.guild)
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
            await message.reply(choice(dunno))  # nosec: B311

    @slash_command(description="Talk to the AI")
    async def ai(self, ctx: ApplicationContext, message: str):
        bucket = self.cd_mapping.get_bucket(ctx)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            return await ctx.respond("Woah, slow down!")
        try:
            print(message)
            response = await self.http.get(
                f"http://api.brainshop.ai/get?bid={self.bid}&key={self.bkey}&uid={ctx.author.id}&msg={message}"
            )
            res = await response.json()
            await ctx.respond(res["cnt"])
        except:
            await ctx.respond(choice(dunno))  # nosec: B311


def setup(client):
    client.add_cog(Chatbot(client))
