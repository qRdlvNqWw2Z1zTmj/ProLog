from discord.ext import commands


class DatabaseCommands:
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def close_db(self):
        await self.config.close()
        await self.prefixes.close()



def setup(bot):
    bot.add_cog(DatabaseCommands(bot))