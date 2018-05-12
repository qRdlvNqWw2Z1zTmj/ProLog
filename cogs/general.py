from discord.ext import commands

class General:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def uh(self):
        pass

def setup(bot):
    bot.add_cog(General(bot))