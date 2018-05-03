import discord
from discord.ext import commands


class MemberUpdateLog:
    def __init__(self, bot):
        self.bot = bot

    async def on_member_update(self, before, after):
        config = await self.bot.config[after.guild.id]
        channels = config.get('MemberUpdateLogs')
        if channels is None: return

        updates = [] #List of embeds to be sent

        if before.nick != after.nick:
            def escapeformat(cont):
                cont = cont.replace('*', '\*')
                cont = cont.replace('__', '\_\_')
                cont = cont.replace('`', '\`')
                cont = cont.replace('~~', '\~\~')
                return cont
            embed = discord.Embed(title=f"User {str(after)} changed their nickname:", description=f"""
            **Before**: {escapeformat(before.nick) if before.nick is not None else escapeformat(before.name)}
**After**: {escapeformat(after.nick)}
            """, color=discord.Color.dark_teal())
            updates.append(embed)

        if before.status != after.status:
            beforestatus = "Online" if before.status == discord.Status.online else "Idle" if before.status == discord.Status.idle else "Do not disturb" if before.status == discord.Status.dnd else "Offline" #IDKKKKKK
            afterstatus = "Online" if after.status == discord.Status.online else "Idle" if after.status == discord.Status.idle else "Do not disturb" if after.status == discord.Status.dnd else "Offline" #Ternary operators in python: "It takes fewer lines!"
            updates.append(discord.Embed(title=f'{str(after)} Changed their status', description=f'''
            **Before**: {beforestatus}
**After**: {afterstatus}
            ''', color=discord.Color.dark_teal()))

        for channel in channels:
            channel = self.bot.get_channel(channel)
            for embed in updates:
                await channel.send(embed=embed)


    @commands.command()
    async def logmembers(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        if await self.bot.config.togglechannel(ctx.guild.id, 'MemberUpdateLogs', channel.id):
            await ctx.send(f'Started logging member updates to <#{channel.id}>!')
        else:
            await ctx.send(f'Stopped logging member updates to <#{channel.id}>')




def setup(bot):
    bot.add_cog(MemberUpdateLog(bot))