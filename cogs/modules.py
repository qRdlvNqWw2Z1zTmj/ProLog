from discord.ext import commands

from .utils.converters import ModuleConverter
from .utils import functions


class Modules:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=["logging", "logs"])
    async def log(self, ctx):
        """The main logging command.
        See the available subcommands and their help pages for more details."""
        if ctx.invoked_subcommand is None:
            await ctx.send("Please provide a valid option. For usage see the help page")

    @log.command(aliases=["set"])
    async def start(self, ctx, *modules: ModuleConverter):
        if len(modules) > 10:
            await ctx.send("No more than 10 modules can be turned on at a time.")
            return

        await functions.module_settings_selection_panel(self, ctx.message, modules, numbered=True)

        ret = await functions.yes_no(self, self.bot, ctx.message)
        print(ret)

    @log.command(aliases=["options"])
    async def settings(self, modules: ModuleConverter):
        pass


def setup(bot):
    bot.add_cog(Modules(bot))
