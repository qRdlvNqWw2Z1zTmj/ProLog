import sys
import traceback

import asyncpg
import discord
from discord.ext import commands

import config
from cogs.utils import dbfunctions

EXTENSIONS = ["cogs.help", "cogs.dev", "cogs.eval", "cogs.general", "cogs.errorhandler",
              "cogs.guildevents", "cogs.events.on_typing"]


class ProLog(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.prefixes = None
        self.config = None
        self.db = None
        super().__init__(*args, **kwargs)

    async def __init(self):
        self.db = await asyncpg.create_pool(config.postgresql)
        self.prefixes = dbfunctions.PrefixesClass(self)
        self.config = dbfunctions.ConfigClass(self)

    async def on_ready(self):
        if self.db is None:
            try:
                await self.__init()
            except TimeoutError as e:
                print(e)
        print('=' * 10)
        print(f'Logged in as {self.user} with the id {self.user.id}')
        print("Logged into PostgresSQL server" if self.db is not None else "Failed to log into PostgreSQl server")
        print(f"Loaded cogs {', '.join([c for c in self.cogs])}")
        print(f'Guild count: {len(self.guilds)}')
        print('=' * 10)


    async def on_message(self, message):
        if not isinstance(message.channel, discord.TextChannel):
            return
        if message.author.bot:
            return
        await self.process_commands(message)
        
    async def prefix(self, message):
        try:
            prefixes = await self.prefixes[message.guild.id]
        except KeyError:
            print('keyerror')
            await self.prefixes.setitem(message.guild.id, ['!'])
            prefixes = self.prefixes[str(message.guild.id)]
        except:
            return commands.when_mentioned(self, message)
        return commands.when_mentioned_or(*prefixes)(self, message)


if __name__ == '__main__':
    bot = ProLog(command_prefix=ProLog.prefix)

    for extension in EXTENSIONS:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()

    try:
        bot.run(config.token)
    finally:
        pass