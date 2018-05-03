import asyncio
import traceback

from discord.ext import commands
from .utils import functions

class Dev:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def logout(self, ctx):
        """Logs the bot out."""
        await ctx.send('Logged out')
        await self.bot.prefixes.close()
        await self.bot.configs.close()
        self.bot.logout()


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


    @commands.command()
    async def reload(self, ctx, module):
        """Reloads a module."""
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
            return
        else:
            await functions.completed(ctx.message)



def setup(bot):
    bot.add_cog(Dev(bot))
