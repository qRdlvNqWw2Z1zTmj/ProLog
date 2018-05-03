import asyncio
import datetime

import discord
from discord.ext import commands


class Typinglog:
    def __init__(self, bot):
        self.bot = bot

    async def on_typing(self, channel, member, when):
        start = datetime.datetime.now()
        if not isinstance(channel, discord.TextChannel): return
        config = await self.bot.config[channel.guild.id]
        channels = config.get('typinglogs')
        if channels is None: return
        try:
            await self.bot.wait_for("message", check=lambda m : m.author == member and m.channel == channel, timeout=10.0)
            return
        except asyncio.TimeoutError:
            if datetime.datetime.now() - start > datetime.timedelta(seconds=10): pass
            else: return
        embed = discord.Embed(title='User started typing:', description=f'''
**User**: {str(member)}
**Channel**: <#{channel.id}>
**Time**: {when.hour}:{when.minute}:{when.second}
**Date**: {when.month}.{when.day}.{when.year}
        ''', color=discord.Color.dark_teal())
        for channel in channels:
            channel = self.bot.get_channel(channel)
            await channel.send(embed=embed)


    @commands.command()
    async def logtyping(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        if await self.bot.config.togglechannel(ctx.guild.id, 'typinglogs', channel.id):
            await ctx.send(f'Started logging typing to <#{channel.id}>!')
        else:
            await ctx.send(f'Stopped logging typing to <#{channel.id}>')
        
        

def setup(bot):
    bot.add_cog(Typinglog(bot))
