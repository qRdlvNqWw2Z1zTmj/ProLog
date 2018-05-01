import datetime

import discord


class GuildEvents:
    def __init__(self, bot):
        self.bot = bot
        self.joinch = None
        
    async def on_guild_join(self, server):
        if self.joinch is None:
            self.joinch = self.bot.get_channel(440217627978366987)
        owner = str(self.bot.get_user(server.owner_id))
        desc = f'Name: {server.name}\nGuild id: {server.id}\nOwner: {owner}\nMember count: {len(server.members)}\n\nJoin time: {datetime.datetime.now()}'
        em = discord.Embed(title='Joined a server!', description = desc, color=discord.Color.green())
        await self.joinch.send(embed=em)

        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(self.bot.guilds)} servers."))

    async def on_guild_remove(self, server):
        if self.joinch is None:
            self.joinch = self.bot.get_channel(440217627978366987)
        owner = str(self.bot.get_user(server.owner_id))
        desc = f'Name: {server.name}\nGuild id: {server.id}\nOwner: {owner}\nMember count: {len(server.members)}\n\nLeave time: {datetime.datetime.now()}'
        em = discord.Embed(title='Left a server.', description = desc, color=discord.Color.red())
        await self.joinch.send(embed=em)

        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(self.bot.guilds)} servers."))



def setup(bot):
    bot.add_cog(GuildEvents(bot))