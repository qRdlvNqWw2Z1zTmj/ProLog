import discord
from discord.ext import commands

from .utils import functions


class General:
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def say(self, ctx, *, arg):
        await ctx.send(arg)
        await ctx.message.delete()

    @commands.group(invoke_without_subcommand=True, aliases=['prefixes', 'pref']) #Fix this seth thx
    async def prefix(self, ctx):
        if ctx.invoked_subcommand is not None:
            return
        prefixes = await self.bot.get_prefix(ctx.message)
        prefixes.remove(f'<@{ctx.guild.me.id}> ') #Not using .mention because it can return <@ID> or <@!ID> 
        prefixes.remove(f'<@!{ctx.guild.me.id}> ')
        stuff = '`\n`'.join(prefixes)
        desc = f'`{stuff}`'
        embed = discord.Embed(title='Prefixes:' if len(prefixes) > 1 else 'Prefix:', description=desc, color=discord.Color.dark_teal())
        await ctx.send(embed=embed)

    @prefix.command(aliases=['create'])
    async def add(self, ctx, prefix):
        try:
            prefs = await self.bot.prefixes[str(ctx.guild.id)]
            prefs.append(prefix)
            prefs.sort()
            await self.bot.prefixes.setitem(ctx.guild.id, list(set(prefs)))
        except KeyError:
            await self.bot.prefixes.setitem(ctx.guild.id, [prefix])

        await functions.completed(ctx.message)

    @prefix.command(aliases=['delete'])
    async def remove(self, ctx, prefix):
        try:
            prefs = await self.bot.prefixes[str(ctx.guild.id)]
            if len(prefs) == 1:
                return await ctx.send('You can\'t have less than one prefix!')
            prefs.remove(prefix)
            await self.bot.prefixes.setitem(ctx.guild.id, prefs)
        except (KeyError, ValueError):
            return await ctx.send(f'Prefix `{prefix}` does not exist.')

        await functions.completed(ctx.message)

def setup(bot):
    bot.add_cog(General(bot))