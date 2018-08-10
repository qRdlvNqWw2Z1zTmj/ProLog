from discord.ext import commands


class Dev:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *, arg):
        "Says something"
        await ctx.send(arg)
        await ctx.message.delete()

    @commands.command()
    async def purge(self, ctx, limit: int):
        """Removes a certain amount of messages."""
        await ctx.channel.purge(limit=limit)


def setup(bot):
    bot.add_cog(Dev(bot))
