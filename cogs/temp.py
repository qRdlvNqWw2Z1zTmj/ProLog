from .utils import functions
from discord.ext import commands

class Temp:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def purge(self, ctx, limit: int):
        """Removes a certain amount of messages."""
        await ctx.channel.purge(limit=limit)



def setup(bot):
    bot.add_cog(Temp(bot))
