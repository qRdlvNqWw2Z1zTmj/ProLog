import asyncio
from operator import attrgetter
from .utils import functions

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
                if command.hidden:
                    continue
                if not command.enabled:
                    continue
            except commands.CommandError:
                continue
            else:
                a = self.cogs.get(command.cog_name)
                if a is None:
                    a = set()
                a.add(command)
                self.cogs[command.cog_name] = a

        unsorted_cogs = self.cogs
        sorted_cogs = {}
        for key in sorted(unsorted_cogs):
            sorted_cogs.update({key: unsorted_cogs[key]})
        self.cogs = sorted_cogs
        self.ready = True

    async def embed_for_cog(self, cogname):
        if not self.ready:
            await self._init()
        commands = self.cogs[cogname]
        embed = discord.Embed(title=f'{cogname} category:', color=discord.Color.dark_teal())
        for command in commands:
            brief = command.__doc__.split('\n')[0] if command.__doc__ is not None else "Unavailable"
            embed.add_field(name=command.name, value=brief, inline=False)
        embed.set_footer(
            text=f'Page {list(self.cogs.keys()).index(cogname) + 1}/{len(self.cogs)}')  # Set embed footer to pagenumber
        fields = sorted(embed.fields, key=attrgetter('name'))  # Sort embed fields by name
        for index, field in enumerate(fields):
            embed.set_field_at(index, name=field.name, value=field.value, inline=field.inline)
        return embed

    async def embed_for_command(self, command):
        if not self.ready:
            await self._init()
        command = self.bot.get_command(command)
        if command is None: return
        embed = discord.Embed(title=f'Help and usage for command `{command.name}`', color=discord.Color.dark_teal())
        embed.add_field(name='Usage:', value=f'{self.ctx.prefix}{command.name} {command.usage}')
        embed.add_field(name='Help:', value=command.help)
        fields = sorted(embed.fields, key=attrgetter('name'))  # Sort embed fields by name
        for index, field in enumerate(fields):
            embed.set_field_at(index, name=field.name, value=field.value, inline=field.inline)
        return embed



class Help:
    def __init__(self, bot):
        self.bot = bot
        self.suggestionch = self.bugreportch = None

    @commands.command()
    async def help(self, ctx, cmd=None):
        """Shows help and usage for commands, or a command list.
        Usage help:
        Argument must be one of the choices mentioned.
        *: Argument is optional
        < >: Argument must be a single item
        [ ]: Argument can be more than one item. Use \"double qoutes\" to include spaces in argument.
        ( ): Same as < >, but spaces are automatically included.
        """
        index = 0
        a = HelpFormatter(ctx)
        await a._init()
        cogs = [cog for cog in a.cogs.keys()]
        cogs.sort()

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

    @commands.command(aliases=['support'])
    async def invite(self, ctx):
        """
        Sends a support server invite and a bot invite
        """
        embed = discord.Embed(title='Invites:', description='[Bot invite](https://discordapp.com/api/oauth2/authorize?client_id=440113872523755520&permissions=0&scope=bot)\n[Support server invite](https://discord.gg/gZESRN5)', color=discord.Color.dark_teal())
        await ctx.send(embed=embed)

    @commands.command()
    async def suggest(self, ctx, *, suggestion):
        """
        Sends a suggestion to the support server
        """
        await functions.completed(ctx.message)
        if self.suggestionch is None:
            self.suggestionch = self.bot.get_channel(440221696184549377)
        await self.suggestionch.send(f'Suggestion by {ctx.author}, id {ctx.author.id}:\n```{suggestion}```')

    @commands.command()
    async def bugreport(self, ctx, *, suggestion):
        """
        Sends a bugreport to the support server
        """
        await functions.completed(ctx.message)
        if self.bugreportch is None:
            self.bugreportch = self.bot.get_channel(440221712056057856)
        await self.bugreportch.send(f'Suggestion by {ctx.author}, id {ctx.author.id}:\n```{suggestion}```')


def setup(bot):
    bot.remove_command('help')
    bot.add_cog(Help(bot))