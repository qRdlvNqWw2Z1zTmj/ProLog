from discord.ext import commands

from .utils.converters import ModuleConverter


class Modules:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=["logging", "logs"])
    async def log(self, ctx):
        """The main logging command.
        See the available subcommands and their help pages for more details."""
        if ctx.invoked_subcommand is None:
            await ctx.send("Please provide a valid option. For usage see the help page")

    @log.command()
    async def start(self, ctx, *module: ModuleConverter):
        if len(module) > 10:
            await ctx.send("No more than 10 modules can be turned on at a time.")
            return

        await ctx.send(f"Would now log {module}")



def setup(bot):
    bot.add_cog(Modules(bot))
