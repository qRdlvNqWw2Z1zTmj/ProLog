import traceback
import importlib

from discord.ext import commands

from .utils import functions
from .utils import database


class Dev:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *, arg):
        "Says something"
        await ctx.send(arg)
        await ctx.message.delete()

    @commands.command()
    async def purge(self, ctx, limit: int):
        """Removes a certain amount of messages."""
        await ctx.channel.purge(limit=limit)

    @commands.command()
    async def logout(self, ctx):
        """Logs the bot out."""
        await self.bot.db.close()
        await functions.completed(ctx.message)
        await self.bot.logout()

    @commands.command()
    async def load(self, ctx, *, module):
        """Loads a module."""
        try:
            self.bot.load_extension(module)
        except:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await functions.completed(ctx.message)

    @commands.command()
    async def unload(self, ctx, *, module):
        """Unloads a module."""
        try:
            self.bot.unload_extension(module)
        except:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await functions.completed(ctx.message)

    @commands.group(invoke_without_command=True)
    async def reload(self, ctx, module):
        if ctx.invoked_subcommand is not None:
            return

        """Reloads a module."""
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
            return
        else:
            await functions.completed(ctx.message)

    @reload.command()
    async def db(self, ctx):
        importlib.reload(database)
        self.bot.DatabaseFunctions = database.DatabaseFunctions(self.bot)
        await functions.completed(ctx.message)

def setup(bot):
    bot.add_cog(Dev(bot))
