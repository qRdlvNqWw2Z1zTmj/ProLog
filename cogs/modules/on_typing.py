class Typinglog:
    def __init__(self, bot):
        self.bot = bot


    async def on_typing(self, channel, member, when):
       pass







        
        

def setup(bot):
    bot.add_cog(Typinglog(bot))
