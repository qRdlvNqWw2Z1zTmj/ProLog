from discord.ext import commands


class DatabaseCommands:
    def __init__(self, bot):
        self.bot = bot




def setup(bot):
    bot.add_cog(DatabaseCommands(bot))