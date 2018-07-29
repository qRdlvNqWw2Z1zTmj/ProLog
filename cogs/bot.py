import re

import discord
from discord.ext import commands

from .utils.database import DatabaseFunctions
from .utils import functions


class BotCommands:
    def __init__(self, bot):
        self.bot = bot
        self.DatabaseFunctions = DatabaseFunctions(bot)
        self.mentions = re.compile("<(@[!&]?|#)(\d{17,21})>")

    @commands.group(aliases=["prefixes"])
    async def prefix(self, ctx):
        if ctx.invoked_subcommand is not None:  return
        prefixes = [x for x in await self.bot.get_prefix(ctx.message) if not self.mentions.match(x)]
        await ctx.send(
            embed=discord.Embed(title='Prefixes:' if len(prefixes) > 1 else 'Prefix:', description="\n".join(prefixes),
                                color=discord.Color.dark_teal()))

    @prefix.command(aliases=['create'])
    async def add(self, ctx, *prefix):
        prefixes = await self.DatabaseFunctions.get_prefixes(self.bot, ctx.message)
        for p in prefix:
            if p not in prefixes and not self.mentions.match(p):
                prefixes.append(p)
        prefixes = [p for p in prefixes if not self.mentions.match(p)]
        await self.DatabaseFunctions.set_item(ctx.guild.id, "configs", "prefixes", prefixes)
        await functions.completed(ctx.message)

    @prefix.command(aliases=['delete'])
    async def remove(self, ctx, *prefix):
        prefixes = await self.DatabaseFunctions.get_prefixes(self.bot, ctx.message)
        await self.DatabaseFunctions.set_item(ctx.guild.id, "configs", "prefixes", [p for p in prefixes if p not in prefix])


def setup(bot):
    bot.add_cog(BotCommands(bot))