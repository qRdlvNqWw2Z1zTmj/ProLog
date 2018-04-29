import discord
from discord.ext import commands


class General:
    def __init__(self, bot):
        self.bot = bot



def setup(bot):
    bot.remove_command('help')
    bot.add_cog(General(bot))