
import discord
from discord.ext import commands
import asyncio
import traceback
import sys
import datetime

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
                await ctx.send('{1.author.mention} Missing permissions: {0}'.format(', '.join(a), ctx))
                return
            elif isinstance(error, commands.MissingPermissions):
                a = []
                for i in error.missing_perms:
                    a.append(' '.join(i.split('_')))
                await ctx.send('{1.author.mention} Missing permissions: {0}'.format(', '.join(a), ctx))
                return
            else:
                return

        elif isinstance(error, commands.TooManyArguments):
            await ctx.send('You gave me too many arguments!')
            return
    
        elif isinstance(error, commands.CommandNotFound):
            if ctx.guild.id in (264445053596991498, 110373943822540800):

                return
            await ctx.send('Command not found.')
            return
        
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send('Command is on cooldown for {} more seconds.'.format(round(error.retry_after, 2)))
            return
        
    
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.author.mention} Missing required argument: {str(error.param).split(":")[0]}')
  
        else:
            msg = f"Guild: {ctx.guild.name}\nGuild ID: {ctx.guild.id}\nChannel: {ctx.channel.name}\nChannel ID:{ctx.channel.id}\nUser: {str(ctx.author)}\nUser ID: {ctx.author.id}\nCommand name: {ctx.command.name}"
            t = traceback.format_exception(type(error), error, error.__traceback__)
            
            a = ' '.join(t)
            e = discord.Embed(timestamp=datetime.datetime.utcnow(), title='An unkown error occured:', description='```'+a+'```', color=discord.Color.red())
            e.add_field(name="Info", value=msg)
            try:
                await self.errorch.send(embed=e)
            except:
                pass
          
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
