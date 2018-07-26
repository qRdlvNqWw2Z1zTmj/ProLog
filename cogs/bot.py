import re

import discord
from discord.ext import commands

from .utils.database import DatabaseFunctions
from .utils.functions import Functions


class BotCommands:
    def __init__(self, bot):
        self.bot = bot
        self.Functions = Functions()
        self.DatabaseFunctions = DatabaseFunctions(bot)
        self.mentions = re.compile("<@!?(\d+)>")

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
            if p in prefixes:
                print(f"Popped {p}")
                prefix.pop(p)
            else:
                prefixes.append(p)
        prefixes = [x for x in prefixes if not self.mentions.match(x)]
        prefixes.sort()
        await self.DatabaseFunctions.set_item(ctx.guild.id, "configs", "prefixes", prefixes)
        await self.Functions.completed(ctx.message)

    @prefix.command(aliases=['delete'])
    async def remove(self, ctx, *prefix):
        pass


def setup(bot):
    bot.add_cog(BotCommands(bot))
