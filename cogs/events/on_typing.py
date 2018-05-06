import asyncio
import datetime

import discord
from discord.ext import commands


class Typinglog:
    def __init__(self, bot):
        self.bot = bot


    async def on_typing(self, channel, member, when):
        if not isinstance(channel, discord.TextChannel):
            return

        print("TYPING!")

        start = datetime.datetime.now()
        config = await self.bot.config[channel.guild.id]






        
        

def setup(bot):
    bot.add_cog(Typinglog(bot))
