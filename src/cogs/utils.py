from discord.ext.commands import Cog, command, is_owner


class Utils(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="reload", hidden=True, aliases=["r"])
    @is_owner()
    async def reload(self, ctx, cog):
        try:
            self.bot.reload_extension(cog)
            await ctx.send(f"Reloaded `cogs.{cog}`")
        except Exception as e:
            await ctx.send(f"Error: {e}")


def setup(bot):
    bot.add_cog(Utils(bot))
