import discord
from discord.ext import commands

from .utils import functions


class DatabaseCommands:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_subcommand=True, aliases=['prefixes', 'pref'])
    async def prefix(self, ctx):
        if ctx.invoked_subcommand is not None:
            return
        prefixes = await self.bot.get_prefix(ctx.message)
        try:
            prefixes.remove(f'<@{self.bot.user.id}> ')
        except ValueError:
            pass
        try:
            prefixes.remove(f'<@!{self.bot.user.id}> ')
        except ValueError:
            pass
        stuff = '`\n`'.join(prefixes)
        desc = f'`{stuff}`'
        embed = discord.Embed(title='Prefixes:' if len(prefixes) > 1 else 'Prefix:', description=desc,
                              color=discord.Color.dark_teal())
        await ctx.send(embed=embed)

    @prefix.command(aliases=['create'])
    async def add(self, ctx, *prefix):
        prefixes = await self.dbfuncs.get_prefixes(self.bot, ctx.message)
        for p in prefix:
            prefixes.append(p)
            prefixes.sort()  # Makes things nice
        prefixes = list(set(prefixes))  # Remove dupes
        await self.dbfuncs.set_prefix(ctx.message, prefixes)
        await functions.completed(ctx.message)

    @prefix.command(aliases=['delete'])
    async def remove(self, ctx, *prefix):
        prefixes = await self.dbfuncs.get_prefixes(self.bot, ctx.message)
        errs = 0
        for p in prefix:
            if p not in prefixes: 
                await ctx.send(f'{p} does not exist!')
                errs += 1
            else:
                prefixes.remove(p)
        await self.dbfuncs.set_prefix(ctx.message, prefixes)
        if len(prefix) == errs: 
            await functions.not_completed(ctx.message)
            return await ctx.send('No prefix was removed!')
        await functions.completed(ctx.message)


def setup(bot):
    bot.add_cog(DatabaseCommands(bot))
