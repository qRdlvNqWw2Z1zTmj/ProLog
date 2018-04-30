from .utils import functions

from discord.ext import commands
import discord

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
        stuff = '**\n**'.join(prefixes)
        desc = f'**{stuff}**'
        embed = discord.Embed(title='Prefixes:' if len(prefixes) > 1 else 'Prefix:', description=desc)
        await ctx.send(embed=embed)

    @prefix.command(aliases=['create'])
    async def add(self, ctx, prefix):
        try:
            prefs = self.bot.prefixes[str(ctx.guild.id)]
            prefs.append(prefix)
            prefs.sort()
            self.bot.prefixes[str(ctx.guild.id)] = list(set(prefs))
        except KeyError:
            self.bot.prefixes[str(ctx.guild.id)] = [prefix]

        await functions.completed(ctx.message)

    @prefix.command(aliases=['delete'])
    async def remove(self, ctx, prefix):
        try:
            prefs = self.bot.prefixes[str(ctx.guild.id)]
            prefs.remove(prefix)
            self.bot.prefixes[str(ctx.guild.id)] = prefs
        except (KeyError, ValueError):
            return await ctx.send(f'Prefix `{prefix}` does not exist.')

        await functions.completed(ctx.message)

def setup(bot):
    bot.add_cog(General(bot))