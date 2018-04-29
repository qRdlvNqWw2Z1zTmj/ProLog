import discord
from discord.ext import commands


class General:
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def say(self, ctx, *, arg):
        await ctx.send(arg)



def setup(bot):
    bot.remove_command('help')
    bot.add_cog(General(bot))