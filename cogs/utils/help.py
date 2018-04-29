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