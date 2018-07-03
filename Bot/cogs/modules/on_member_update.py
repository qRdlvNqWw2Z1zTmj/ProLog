class MemberUpdateLog:
    def __init__(self, bot):
        self.bot = bot

    async def on_member_update(self, before, after):
        pass









def setup(bot):
    bot.add_cog(MemberUpdateLog(bot))