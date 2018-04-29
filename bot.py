import discord
from config import token
from discord.ext import commands
import aiohttp
import config

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def on_ready(self):
        print('='*10)
        print(f'Logged in as {self.user} with the id {self.user.id}')
        print(f'Guild count: {len(self.guilds)}')
        print('='*10)

    async def on_message(self, message):
        if not isinstance(message.channel, discord.TextChannel):
            return
        if message.author.bot:
            return
        
        await self.process_commands(message)

if __name__ == '__main__':
    bot = Bot(command_prefix='?')
    bot.run(config.token)
