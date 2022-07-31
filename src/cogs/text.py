from discord.ext.commands import Cog, Context # type: ignore
from discord.ext.bridge.core import bridge_command
from random import choice

from bot import PogBot


class Text(Cog):
    def __init__(self, bot: PogBot):
        self.bot = bot

    @bridge_command(description="Reverse the text!")
    async def reverse(self, ctx, *, s: str):
        result = s[::-1]
        if len(result) <= 350:
            await ctx.send(f"{result}")
        else:
            try:
                await ctx.author.send(f"{result}")
                await ctx.send(
                    f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**"
                )
            except Exception:
                await ctx.send(
                    f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**"
                )

    @bridge_command(description="Convert text to binary!", aliases=["ttb"])
    async def texttobinary(self, ctx, *, s):
        try:
            cleanS = " ".join(format(ord(x), "b") for x in s)
        except Exception as e:
            await ctx.send(
                f"**Error: `{e}`. This probably means the text is malformed. Sorry, you can always try here: http://www.unit-conversion.info/texttools/convert-text-to-binary/#data**"
            )
        if len(cleanS) <= 479:
            await ctx.send(f"```fix\n{cleanS}```")
        else:
            try:
                await ctx.author.send(f"```fix\n{cleanS}```")
                await ctx.send(
                    f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**"
                )
            except Exception:
                await ctx.send(
                    f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**"
                )

    @bridge_command(description="Convert binary to text!", aliases=["btt"])
    async def binarytotext(self, ctx, *, s):
        try:
            cleanS = "".join([chr(int(s, 2)) for s in s.split()])
        except Exception as e:
            await ctx.send(
                f"**Error: `{e}`. This probably means the text is malformed. Sorry, you can always try here: http://www.unit-conversion.info/texttools/convert-text-to-binary/#data**"
            )
        if len(cleanS) <= 479:
            await ctx.send(f"```{cleanS}```")
        else:
            try:
                await ctx.author.send(f"```{cleanS}```")
                await ctx.send(
                    f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**"
                )
            except Exception:
                await ctx.send(
                    f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**"
                )

    @bridge_command(aliases=["e"])
    async def encrypt(self, ctx, *, s):
        try:
            cleanS = "".join(chr(ord(letter) + len(s)) for letter in s)
        except Exception as e:
            return await ctx.send(
                f"**Error: `{e}`. This probably means the input is malformed. Sorry, I'm not perfect and my creator is dumb**"
            )
        if len(cleanS) <= 479:
            await ctx.send(f"```{cleanS}```")
        else:
            try:
                await ctx.author.send(f"```{cleanS}```")
                await ctx.send(
                    f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**"
                )
            except Exception:
                await ctx.send(
                    f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**"
                )

    @bridge_command(aliases=["d"])
    async def decrypt(self, ctx, *, s):
        try:
            cleanS = "".join(chr(ord(letter) - len(s)) for letter in s)
        except Exception as e:
            return await ctx.send(
                f"**Error: `{e}`. This probably means the input is malformed.**"
            )
        if len(cleanS) <= 479:
            await ctx.send(f"```{cleanS}```")
        else:
            try:
                await ctx.author.send(f"```{cleanS}```")
                await ctx.send(
                    f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**"
                )
            except Exception:
                await ctx.send(
                    f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**"
                )

    @bridge_command()
    async def drunkify(self, ctx: Context, *, s: str):
        lst = (str.upper, str.lower)
        newText = "".join(choice(lst)(c) for c in s)
        if len(newText) <= 380:
            await ctx.send(newText)
        else:
            try:
                await ctx.author.send(newText)
                await ctx.send(
                    f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**"
                )
            except Exception:
                await ctx.send(
                    f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**"
                )


def setup(bot):
    bot.add_cog(Text(bot))
