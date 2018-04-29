import asyncio
import traceback

from discord.ext import commands


class Dev:
    def __init__(self, bot):
        self.bot = bot


    @commands.command(help='Logs the bot out.', usage='')
    async def logout(self, ctx):
        """Logs the bot out."""
        await ctx.send('Logging out bai')
        self.bot.update = False
        await asyncio.sleep(60)
        self.bot.living_file.close()
        self.bot.pref_file.close()
        await ctx.send('Logged out')
        self.bot.logout()


    @commands.command(help='Loads an module.', usage='<module>')
    async def load(self, ctx, *, module):
        """Loads a module."""
        try:
            self.bot.load_extension(module)
        except:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send('\N{OK HAND SIGN}')


    @commands.command(help='Unloads an module.', usage='<module>')
    async def unload(self, ctx, *, module):
        """Unloads a module."""
        try:
            self.bot.unload_extension(module)
        except:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send('\N{OK HAND SIGN}')


    @commands.command(help='Reloads a module', usage='<module>')
    async def reload(self, ctx, module: str):
        """Reloads a module."""
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
            return
        await ctx.send(f"Successfully reloaded module {module} {ctx.author.mention}")





def setup(bot):
    bot.add_cog(Dev(bot))