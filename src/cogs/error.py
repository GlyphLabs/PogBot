from discord.ext import commands
from discord import HTTPException, Embed
import sys
from traceback import print_exception
from humanize import naturaldelta

from bot import PogBot


class Error(commands.Cog):
    def __init__(self, bot: PogBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        if hasattr(ctx.command, "on_error"):
            return

        ignored = commands.UserInputError
        error = getattr(error, "original", error)

        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.respond(
                f"**:no_entry: `{ctx.command}` has been disabled.**"
            )

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(
                    f"**:no_entry: `{ctx.command}` can not be used in Private Messages.**"
                )
            except HTTPException:
                pass
        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == "tag list":
                return await ctx.respond(
                    "**:no_entry: I could not find that member. Please try again.**"
                )
        elif isinstance(error, commands.BotMissingPermissions):
            return await ctx.respond(
                f"**:no_entry: Oops, I need `{error.missing_perms[0].replace('_', ' ')}` permission to run this command**"
            )
        elif isinstance(error, commands.CommandOnCooldown):
            return await ctx.respond(
                f"**:no_entry: Woah there, that command is on a cooldown for {naturaldelta(error.retry_after)}!**"
            )
        elif isinstance(error, commands.CheckFailure) or isinstance(
            error, commands.MissingPermissions
        ):
            return await ctx.respond(
                f"**:no_entry: You can't use that command, you're missing the {', '.join(error.missing_perms.upper())} permissions**"
            )
        elif isinstance(error, commands.CommandInvokeError):
            return await ctx.respond(
                f"**:no_entry: not pog! :((\ni made an oopsie: \\\\ \n  {error}**"
            )
        else:
            embed = Embed(
                title="**Oh no...**",
                description="Something went wrong! The devs have been notified and will deal with the problem shortly.\n**Need extra help?** Join the [**Support Server**](https://discord.gg/bNtj2nFnYA)",
            )
            embed.add_field(name="error", value=f"```{error}```")
            await ctx.send(embed=embed)
            print(
                "Ignoring exception in command {}:".format(ctx.command), file=sys.stderr
            )
            print("=" * 25)
            print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            print("=" * 25)


def setup(bot):
    bot.add_cog(Error(bot))
