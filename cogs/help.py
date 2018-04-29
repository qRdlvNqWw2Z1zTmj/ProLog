import asyncio
from operator import attrgetter

import discord
from discord.ext import commands


class HelpFormatter:
    def __init__(self, ctx):
        self.ctx = ctx
        self.bot = ctx.bot
        self.cogs = {}
        self.ready = False

    async def _init(self):
        for command in self.bot.commands:
            try:
                await command.can_run(self.ctx)
            except commands.CommandError:
                continue
            else:
                a = self.cogs.get(command.cog_name)
                if a is None:
                    a = set()
                a.add(command)
                self.cogs[command.cog_name] = a

        self.ready = True

    async def embed_for_cog(self, cogname):
        if not self.ready:
            await self._init()
        commands = self.cogs[cogname]
        embed = discord.Embed(title=f'{cogname} category:', color=discord.Color.dark_teal())
        for command in commands:
            embed.add_field(name=command.name, value=command.short_doc if command.short_doc is not None else 'Unavailable', inline=False)
        embed.set_footer(
            text=f'Page {list(self.cogs.keys()).index(cogname) + 1}/{len(self.cogs)}')  # Set embed footer to pagenumber
        sorted(embed.fields, key=attrgetter('name'))  # Sort embed fields by name
        return embed

    async def embed_for_command(self, command):
        if not self.ready:
            await self._init()
        command = self.bot.get_command(command)
        if command is None: return
        embed = discord.Embed(title=f'Help and usage for command `{command.name}`', color=discord.Color.dark_teal())
        embed.add_field(name='Usage:', value=f'{self.ctx.prefix}{command.name} {command.usage}')
        embed.add_field(name='Help:', value=command.help)
        sorted(embed.fields, key=attrgetter('name'))  # Sort embed fields by name
        return embed



class Help:
    def __init__(self, bot):
        self.bot = bot


    @commands.command(help="Shows help and usage for commands, or a command list.\nUsage help:\n/: Argument must be one of the choices mentioned.\n*: Argument is optional\n< >: Argument must be a single item\n[ ]: Argument can be more than one item. Use \"double qoutes\" to include spaces in argument.\n( ): Same as < >, but spaces are automatically included.", usage="*<command>")
    async def help(self, ctx, cmd=None):
        index = 0
        a = HelpFormatter(ctx)
        await a._init()
        cogs = [cog for cog in a.cogs.keys()]

        async def interactive(formatter, msg, index, cogs, info):
            msg = await ctx.channel.get_message(msg.id)
            if len(cogs) == index: index -= 1
            if index == -1: index = 0
            em = await formatter.embed_for_cog(cogs[index])
            if info:
                info = False
            await msg.edit(embed=em)
            try:
                reacts = ['\U000023ee', '\U000025c0', '\U000025b6', '\U000023ed', '\U000023f9', '\U00002139']
                onmsg = [r.emoji for r in msg.reactions]
                for r in [r for r in reacts if r not in onmsg]:
                    await msg.add_reaction(r)

                def check(r, u):
                    return r.emoji in reacts and u.id == ctx.author.id and r.message.id == msg.id

                r, u = await self.bot.wait_for('reaction_add', check=check, timeout=10000)
                if r.emoji == '\U000023ee':  # Track previous
                    index = 0
                elif r.emoji == '\U000025c0':  # Left arrow
                    index -= 1
                elif r.emoji == '\U000025b6':  # Right arrow
                    index += 1
                elif r.emoji == '\U000023ed':  # Track next
                    index = len(cogs) - 1
                elif r.emoji == '\U000023f9':  # Stop
                    await msg.delete()
                    return await ctx.message.delete()
                elif r.emoji == '\U00002139':  # Info
                    em = discord.Embed(color=discord.Color.blue(), title='Info:',
                                       description=f'\nUse the buttons to switch pages.\nThe ⏹️button ends the interactive session.\nUse `{ctx.prefix}help <command>` to get help and usage on a specific command.')
                    await msg.edit(embed=em)
                    try:
                        await msg.clear_reactions()
                    except discord.Forbidden:
                        pass
                    await msg.add_reaction('\U0000274c')

                    def check1(r, u):
                        return r.emoji == '\U0000274c' and u.id == ctx.author.id and r.message.id == msg.id

                    await self.bot.wait_for('reaction_add', check=check1, timeout=10000)
                    try:
                        await msg.clear_reactions()
                    except discord.Forbidden:
                        pass

                    info = True
                try:
                    await msg.remove_reaction(r.emoji, u)
                except discord.Forbidden:
                    pass

            except asyncio.TimeoutError:
                try:
                    await msg.clear_reactions()
                except discord.Forbidden:
                    pass
                return

            await interactive(formatter, msg, index, cogs, info)

        if cmd is None:
            msg = await ctx.send(embed=await a.embed_for_cog(cogs[index]))
            return await interactive(a, msg, index, cogs, False)

        embed = await a.embed_for_command(cmd)
        if embed is None:
            return await ctx.send(f'Could not find command `{cmd}`')
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Help(bot))