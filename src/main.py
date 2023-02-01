from bot import PogBot

bot = PogBot()

for cog in bot.ext:
    try:
        bot.load_extension(f"cogs.{cog}")
        print(f"loaded cogs.{cog}")
    except Exception as e:
        print(f"error loading cogs.{cog}: {e}")

bot.run()
