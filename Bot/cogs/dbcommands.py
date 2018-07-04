import discord
from discord.ext import commands
from .utils import functions
import re

class DatabaseCommands:
    def __init__(self, bot):
        self.bot = bot
        self.dbfuncs = bot.dbfuncs
        self.pattern = re.compile(r"<..?[0-9]{18}>")

    def clean(self, prefixes: list):
        try:
            prefixes.remove(f'<@{self.bot.user.id}> ')
        except ValueError:
            pass
        try:
            prefixes.remove(f'<@!{self.bot.user.id}> ')
        except ValueError:
            pass
        return prefixes

    @commands.group(invoke_without_subcommand=True, aliases=['prefixes', 'pref'])
    async def prefix(self, ctx):
        if ctx.invoked_subcommand is not None:
            return
        prefixes = self.clean(await self.bot.get_prefix(ctx.message))
        stuff = '`\n`'.join(prefixes)
        desc = f'`{stuff}`'
        embed = discord.Embed(title='Prefixes:' if len(prefixes) > 1 else 'Prefix:', description=desc,
                              color=discord.Color.dark_teal())
        await ctx.send(embed=embed)

    @prefix.command(aliases=['create'])
    async def add(self, ctx, *prefix):
        prefixes = self.clean(await self.dbfuncs.get_prefixes(self.bot, ctx.message))
        added = 0

        for p in prefix:
            if self.pattern.match(p):
                await ctx.send('Prefix cannot be any kind of mention.')
                continue

            prefixes.append(p)
            added +=1

        prefixes.sort()  # Makes things nice
        prefixes = list(set(prefixes))  # Remove dupes

        if added != 0:
            await self.dbfuncs.set_prefix(ctx.message, prefixes)
            return await functions.completed(ctx.message)
        
        await ctx.send('No prefixes were added.')
        await functions.not_completed(ctx.message)

    @prefix.command(aliases=['delete'])
    async def remove(self, ctx, *prefix):
        prefixes = self.clean(await self.dbfuncs.get_prefixes(self.bot, ctx.message))
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
