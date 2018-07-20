class MemberUpdateLog:
    def __init__(self, bot):
        self.bot = bot

    async def on_member_update(self, before, after):
        if before.name != after.name:
            await self.UpdateName(before, after)

        if before.nick != after.nick:
            await self.UpdateNick(before, after)

        if before.status != after.status:
            await self.UpdateStatus(before, after)

        if before.activity != after.activity:
            await self.UpdateActivity(before, after)

        if before.roles != after.roles:
            await self.UpdateRole(before, after)

    async def UpdateName(self, before, after):
        pass

    async def UpdateNick(self, before, after):
        pass
    
    async def UpdateStatus(self, before, after):
        pass

    async def UpdateActivity(self, before, after):
        pass

    async def UpdateRole(self, before, after):
        pass









def setup(bot):
    bot.add_cog(MemberUpdateLog(bot))