import datetime
import sys
import traceback

import discord
from discord.ext import commands


class ErrorHandler:
    def __init__(self, bot):
        self.bot = bot
        self.errorch = None

    async def on_command_error(self, ctx, error):
        if self.errorch is None:
            self.errorch = self.bot.get_channel(440200135604043797)

        ignored = (discord.Forbidden)
    
        if isinstance(error, ignored):
            return
            
        elif isinstance(error, commands.CheckFailure):
            if isinstance(error, commands.NotOwner):
                a = []
                for i in error.missing_perms:
                    a.append(' '.join(i.split('_')))
                await ctx.send(f'{ctx.author.mention} Missing permissions: {", ".join(a)}')
                return
            elif isinstance(error, commands.MissingPermissions):
                a = []
                for i in error.missing_perms:
                    a.append(' '.join(i.split('_')))
                await ctx.send(f'{ctx.author.mention} Missing permissions: {", ".join(a)}')
                return
            else:
                return

        elif isinstance(error, commands.TooManyArguments):
            await ctx.send('You passed too many arguments')
            return

        
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'Command is on cooldown for {round(error.retry_after, 2)} more seconds.')
            return

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'Required argument {str(error.param).split(":")[0]} is missing. See {self.bot.command_prefix[0]}help {ctx.command.name} for usage')


        else:
            msg = f"Guild: {ctx.guild.name}\nGuild ID: {ctx.guild.id}\nChannel: {ctx.channel.name}\nChannel ID:{ctx.channel.id}\nUser: {str(ctx.author)}\nUser ID: {ctx.author.id}\nCommand name: {ctx.command.name if ctx.command is not None else None}"
            t = traceback.format_exception(type(error), error, error.__traceback__)
            
            a = ' '.join(t)
            e = discord.Embed(timestamp=datetime.datetime.utcnow(), title='An unkown error occured:', description='```'+a+'```', color=discord.Color.red())
            e.add_field(name="Info", value=msg)
            try:
                await self.errorch.send(embed=e)
            except:
                pass
          
        print('Ignoring exception in command {ctx.command}:', file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
