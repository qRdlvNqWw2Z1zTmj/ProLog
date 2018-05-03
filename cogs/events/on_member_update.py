import discord
from discord.ext import commands


class MemberUpdateLog:
    def __init__(self, bot):
        self.bot = bot

    async def on_member_update(self, before, after):
        config = await self.bot.config[after.guild.id]
        channels = config.get('MemberUpdateLogs')
        if channels is None: return


        if before.nick != after.nick:
            embed = discord.Embed(title=f"User {str(after)} changed their nickname:", description=f"""
            **Before**: `{before.nick if before.nick is not None else str(before.name)}`
**After**: `{after.nick}`
            """, color=discord.Color.dark_teal())
            for channel in channels:
                channel = self.bot.get_channel(channel)
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