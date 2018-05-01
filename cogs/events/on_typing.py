import discord
from discord.ext import commands

class Typinglog:
    def __init__(self, bot):
        self.bot = bot

    async def on_typing(self, channel, user, when):
        if not isinstance(channel, discord.TextChannel): return
        channels = await self.bot.config.get(channel.guild.id)
        if channels is None: return
        embed = discord.Embed(title='User started typing:', description=f'''
        **User**: {str(user)}
        **Channel**: <#{channel.id}>
        **Time**: {when.hour}:{when.minute}:{when.second}
        **Date**: {when.month}.{when.day}.{when.year}
        ''', color=discord.Color.dark_teal())

        for channel in channels:
            await channel.send(embed=embed)

    @commands.command()
    async def logtyping(self):
        pass