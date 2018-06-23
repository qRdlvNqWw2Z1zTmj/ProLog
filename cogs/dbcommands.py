import discord
from discord.ext import commands
from discord.ext.commands import TextChannelConverter

from .utils import dbfunctions
from .utils import functions


class DatabaseCommands:
    def __init__(self, bot):
        self.bot = bot
        self.dbfuncs = dbfunctions.DatabaseFunctions(bot)

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




    @commands.group(aliases=["logging", "logs"])
    async def log(self, ctx):
        """The main logging command.
        See the available subcommands and their help pages for more details."""
        if ctx.invoked_subcommand is None:
            await ctx.send("Please provide a valid option. For usage see the help page")

    @log.command()
    async def start(self, ctx, *args):
        """Starts lmodule logging in specified channels.
        It does not matter in what order the modules and channels are in, as long as they're correct and separated by spaces the command will work.
        A list of modules and module catagories can be shown with ."""
        modules = []
        channels = []
        badargs = []
        uploaddict = {}

        # Parse args (I could make this Regex. I'm not sure yet)
        for a in args:
            try:
                channel = await TextChannelConverter().convert(ctx, a)
                channels.append(channel)
                print(f"Added channel {channel}")
            except discord.ext.commands.errors.BadArgument:
                print(f"Module keys: {[x for x in self.bot.modules.keys()]}")
                if not a.casefold() in map(str.casefold, [x for x in self.bot.modules.keys()]):
                    badargs.append(a)
                else:
                    # Fix random cases
                    for m in self.bot.modules:
                        if a.lower() == m.lower():
                            a = m
                    print(f"New module {a}")
                    modules.append(a)


        # Error on no channels
        if not channels:
            await ctx.send("Please provide a channel mention, name or id")
            return

        # Error on no modules
        if not modules:
            await ctx.send("Please provide a valid module")
            return



        # Say on bad args
        if badargs:
            await ctx.send(f"Invalid argument `{badargs[0]}`. Ignoring" if len(badargs) == 1 else
                           f"Invalid arguments `{', '.join([b for b in badargs])}`. Ignoring" if badargs > 1 else None)

        # Confirmation message
        if modules:
            await ctx.send(f"Started logging modules "
                           f"{', '.join([m for m in modules])} in {', '.join([c.mention for c in channels])}")



        # Construct dict
        for m in modules:
            uploaddict[m] = [c.id for c in channels]

        print(uploaddict)

        await self.dbfuncs.set_item(ctx.guild.id, "configs", "modules", dict)

        await ctx.send(f"Dict that would be JSON'd then uploaded: {dict}")



    @log.group()
    async def show(self, ctx):
        await ctx.send('WIP')

    @show.command()
    async def all(self, ctx):
        await ctx.send('WIP')


def setup(bot):
    bot.add_cog(DatabaseCommands(bot))
