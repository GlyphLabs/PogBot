from discord.ext.commands.help import HelpCommand
from discord import Embed, Colour
from .buttons import HelpButtons


class PogBotHelp(HelpCommand):
    def get_command_signature(self, command):
        return f"{self.context.clean_prefix}{command.qualified_name}"

    async def send_bot_help(self, mapping):
        embed = Embed(title="PogBot Help", color=Colour.random())
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            command_signatures = [self.get_command_signature(c) for c in filtered]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category").replace(
                    "_", " "
                )
                embed.add_field(
                    name=cog_name.capitalize(),
                    value="`" + "`, `".join(command_signatures) + "`",
                    inline=False,
                )
        channel = self.get_destination()
        await channel.send(embed=embed, view=HelpButtons())

    async def send_cog_help(self, cog):
        embed = Embed(
            title=f"{cog.qualified_name} - PogBot Help", color=Colour.random()
        )
        for command in cog.get_commands():
            if not command.description:
                desc = "None"
            else:
                desc = command.description
            embed.add_field(name=command.name.lower(), value=desc, inline=True)
        channel = self.get_destination()
        await channel.send(embed=embed, view=HelpButtons())

    async def send_command_help(self, command):
        embed = Embed(title=f"{command.name}", color=Colour.random())
        if command.aliases:
            embed.add_field(
                name="Aliases", value=", ".join(command.aliases), inline=False
            )
        if command.description:
            embed.add_field(name="Help", value=command.description)
        channel = self.get_destination()
        await channel.send(embed=embed, view=HelpButtons())
