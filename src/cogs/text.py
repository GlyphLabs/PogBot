from discord.ext import commands


class TextManipulation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def reverse(self, ctx, *, s: commands.clean_content):
        result = await commands.clean_content().convert(ctx, s[::-1])
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

    @commands.command()
    async def texttobinary(self, ctx, *, s):
        try:
            cleanS = await commands.clean_content().convert(
                ctx, " ".join(format(ord(x), "b") for x in s)
            )
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

    @commands.command()
    async def binarytotext(self, ctx, *, s):
        try:
            cleanS = await commands.clean_content().convert(
                ctx, "".join([chr(int(s, 2)) for s in s.split()])
            )
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

    async def specrypt(ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(
                "```fix\nInvalid input. Please use one of the following:\nencrypt (e)\ndecrypt (d)\n\nExample: $specrypt e Hello world!```"
            )

    @commands.command(aliases=["e"])
    async def encrypt(self, ctx, *, s):
        a = ""
        try:
            for letter in s:
                a += chr(ord(letter) + len(s))
            cleanS = await commands.clean_content().convert(ctx, a)
        except Exception as e:
            await ctx.send(
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

    @commands.command(aliases=["d"])
    async def decrypt(self, ctx, *, s):
        a = ""
        try:
            for letter in s:
                a += chr(ord(letter) - len(s))
            cleanS = await commands.clean_content().convert(ctx, a)
        except Exception as e:
            await ctx.send(
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


def setup(bot):
    bot.add_cog(TextManipulation(bot))
