import re
from discord.ext import commands
import discord


class BotCommands:
    def __init__(self, bot):
        self.bot = bot
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

    @commands.group(invoke_without_subcommand=True, aliases=['prefixes', 'pref'], usage='<add/remove>')
    async def prefix(self, ctx):
        """Show ."""
        if self.bot.dbfuncs is None:
            return await ctx.send('Custom prefixes are unavailable.\nFor now, use prefix !')
        if ctx.invoked_subcommand is not None:
            return
        w = 30
        prefixes = self.clean(await self.bot.get_prefix(ctx.message))
        stuff = '"\n"'.join(prefixes)
        desc = f'"{stuff}"'.ljust(w)
        embed = discord.Embed(title='Prefixes:' if len(prefixes) > 1 else 'Prefix:', description=desc,
                              color=discord.Color.dark_teal())
        await ctx.send(embed=embed)

    @prefix.command(aliases=['create'])
    async def add(self, ctx, *prefix):
        if self.bot.dbfuncs is None:
            return await ctx.send('Custom prefixes are unavailable.\nFor now, use prefix !')
        prefixes = self.clean(await self.bot.functions.get_prefixes(self.bot, ctx.message))
        added = 0

        for p in prefix:
            if self.pattern.match(p) or p in ['@everyone', '@here']:
                await ctx.send('Prefix cannot be any kind of mention.')
                continue

            prefixes.append(p)
            added += 1

        prefixes.sort()  # Makes things nice
        prefixes = list(set(prefixes))  # Remove dupes

        if added:
            await self.bot.functions.set_prefix(ctx.message, prefixes)
            suff = 'es' * bool(added - 1)
            await ctx.send(f'{added} prefix{suff} added')
            return await self.bot.functions.completed(ctx.message)

        await ctx.send('No prefixes were added.')
        await self.bot.functions.not_completed(ctx.message)

    @prefix.command(aliases=['delete'])
    async def remove(self, ctx, *prefix):
        if self.bot.dbfuncs is None:
            return await ctx.send('Custom prefixes are unavailable.\nFor now, use prefix !')
        prefixes = self.clean(await self.bot.functions.get_prefixes(self.bot, ctx.message))
        removed = 0
        for p in prefix:
            if p not in prefixes:
                await ctx.send(f'{p} does not exist!')

            else:
                prefixes.remove(p)
                removed += 1
        await self.bot.functions.set_prefix(ctx.message, prefixes)
        if not removed:
            await self.bot.functions.not_completed(ctx.message)
            return await ctx.send('No prefix was removed!')

        suff = 'es' * bool(removed - 1)
        await ctx.send(f'{removed} prefix{suff} removed!')
        await self.bot.functions.completed(ctx.message)



def setup(bot):
    bot.add_cog(BotCommands(bot))
