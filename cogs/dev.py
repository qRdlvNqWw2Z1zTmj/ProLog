import io, asyncio
import textwrap
import traceback
from contextlib import redirect_stdout

from discord.ext import commands


class Eval:
    def __init__(self, bot):
        self.bot = bot

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # Remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])


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


    @commands.command(hidden=True, name='eval')
    async def _eval(self, ctx, *, body: str):
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')



def setup(bot):
    bot.add_cog(Eval(bot))