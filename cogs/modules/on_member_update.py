import discord
from discord.ext import commands
from ..utils import dbfunctions

class MemberUpdateLog:
    def __init__(self, bot):
        self.bot = bot
        self.dbfuncs = dbfunctions.DatabaseFunctions(bot)

    async def on_member_update(self, before, after):










def setup(bot):
    bot.add_cog(MemberUpdateLog(bot))