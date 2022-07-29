from discord.ext.commands import Bot, when_mentioned_or, Context
from discord import Message, Intents
from asyncio import sleep
from discord import utils
from typing import List
from helpcmd import PogBotHelp
from time import time
from os import environ


class PogBot(Bot):
    def __init__(self, extensions: List[str] = None):
        super().__init__(
            command_prefix=when_mentioned_or("."),
            case_insensitive=True,
            intents=Intents.all(),
            owner_ids=(
                536644802595520534,  # thrizzle.#4258
                819786180597907497,  # griffin#1405
                656021685203501066,  # RyZe#7968
                839514280251359292,  # Random_1s#999
            ),
        )
        self.ext = extensions or ("chatbot", "error", "meme", "text", "economy")
        self.poglist = (
            "pog",
            "pogger",
            "poggers",
            "pogg",
            "poger",
            "poggus",
        )
        self.statuses = (
            "you pog",
            "us grow",
            "yuno miles music videos",
            "thrzl break stuff",
            "for 'pog'",
        )
        self.help_command = PogBotHelp()

    async def check(self, ctx: Context):
        if ctx.author.bot or not ctx.guild:
            return False
        return True

    async def on_message(self, message: Message) -> None:
        if message.author.bot:
            return
        await self.process_commands(message)
        for i in [c.name.lower() for c in self.commands]:
            if message.content.lower() in [f"pog{i}", f"pog {i}"]:
                return
        for word in message.content.lower().split(" "):
            if word in self.poglist:
                await sleep(1)
                custom_emoji = utils.get(self.emojis, name="POG")
                await message.add_reaction(custom_emoji)
        if message.content == "family":
            await message.channel.send(
                "https://tenor.com/view/i-dont-have-friends-i-have-family-theyre-not-my-friends-theyre-my-family-more-than-friends-gif-16061717"
            )

    def load_extension(self, name: str):
        super().load_extension(f"cogs.{name}")

    def reload_extension(self, name: str):
        self.unload_extension(name)
        self.load_extension(name)

    def unload_extension(self, name: str):
        super().unload_extension(f"cogs.{name}")

    def run(self):
        token = environ.get("TOKEN")
        super().load_extension("jishaku")
        for ext in self.ext:
            self.load_extension(ext)
        self.start_time = time()
        super().run(token)
