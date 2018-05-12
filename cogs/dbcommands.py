import discord
from discord.ext import commands
from discord.ext.commands import TextChannelConverter

from .utils import dbfunctions
from .utils import functions


class DatabaseCommands:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def getitem(self, ctx, table, column, item, guildid: int = None):
        if guildid is None:
            guildid = ctx.guild.id
        await ctx.send(await dbfunctions.DatabaseFunctions(self).get_row(guildid, table, column, item, ))


    @commands.group(invoke_without_subcommand=True, aliases=['prefixes', 'pref'])
    async def prefix(self, ctx):
        if ctx.invoked_subcommand is not None:
            return
        prefixes = await self.bot.get_prefix(ctx.message)
        stuff = '`\n`'.join(prefixes)
        desc = f'`{stuff}`'
        embed = discord.Embed(title='Prefixes:' if len(prefixes) > 1 else 'Prefix:', description=desc,
                              color=discord.Color.dark_teal())
        await ctx.send(embed=embed)

    @prefix.command(aliases=['create'])
    async def add(self, ctx, *prefix):
        prefixes = await dbfunctions.DatabaseFunctions(self.bot).get_prefixes(self, ctx.message)
        for p in prefix:
            prefixes.append(p)
            prefixes.sort() #Makes things nice
        prefixes = list(set(prefixes)) #Remove dupes
        await dbfunctions.DatabaseFunctions(self.bot).set_item(ctx.guild.id, "configs", "prefixes", prefixes)
        await functions.completed(ctx.message)

    @prefix.command(aliases=['delete'])
    async def remove(self, ctx, *prefix):
        prefixes = await dbfunctions.DatabaseFunctions(self.bot).get_prefixes(self, ctx.message)
        for p in prefix:
            if p not in prefixes: print(f'{p} not in db or whatever')
            else: prefixes.remove(p)
        await dbfunctions.DatabaseFunctions(self.bot).set_item(ctx.guild.id, "configs", "prefixes", prefixes)
        await functions.completed(ctx.message)



    @commands.group()
    async def log(self, ctx):
        """The main logging command."""
        if ctx.invoked_subcommand is None:
            await ctx.send("Please provide a valid option")

    @log.command()
    async def start(self, ctx, *args):
        """Starts logging specified modules in specified channels.
        It doesn't matter in what order the modules and channels are in, as long as they're correct and separated by spaces it will succeed.
        A list of modules and module catagories can be shown with the command `log show all`."""
        mods = []
        channels = []
        badargs = []

        # Parse the mash of arguments
        for m in args:
            try:
                channel = await TextChannelConverter().convert(ctx, m)
                channels.append(channel)
            except commands.errors.BadArgument:
                if not m.casefold() in map(str.casefold, self.bot.modules):
                    print(f"Bad argument: {m}")
                    badargs.append(m)
                else:
                    mods.append(m)

        # Update the guild configs
        for c in channels:
            for m in mods:
                print(f"Channel: {c.name} {c.id} GuildID: {c.guild.id} Module: {m}")
                await self.togglechannel(c.guild.id, m, c.id)

        # Error on no channels
        if not channels:
            await ctx.send("No channels specified")
            return

        # Error on bad args
        if badargs:
            await ctx.send(f"Invalid argument `{badargs[0]}`. Ignoring" if len(badargs) == 1 else
                           f"Invalid arguments `{', '.join([b for b in badargs])}`. Ignoring" if badargs > 1 else None)

        # Confirmation message
        if mods:
            await ctx.send(f"Started logging modules {', '.join([m for m in mods])} in {', '.join([c.mention for c in channels])}")


    @log.group()
    async def show(self, ctx):
        await ctx.send('WIP')
    
    @show.command()
    async def all(self, ctx):
        await ctx.send('WIP')

def setup(bot):
    bot.add_cog(DatabaseCommands(bot))