import discord
from discord.ext import commands


class MemberUpdateLog:
    def __init__(self, bot):
        self.bot = bot


    async def on_member_update(self, before, after):
        config = await self.bot.config[after.guild.id]











def setup(bot):
    bot.add_cog(MemberUpdateLog(bot))