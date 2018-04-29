from discord.ext import commands

class General:
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def say(self, ctx, *, arg):
        await ctx.send(arg)
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(General(bot))