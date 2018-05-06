import asyncio
import sys
import traceback

import asyncpg
import discord
from discord.ext import commands

import config
from cogs.utils import dbfunctions

cogs = ["cogs.help", "cogs.dev", "cogs.eval", "cogs.general", "cogs.errorhandler",
              "cogs.guildevents", "cogs.events.on_typing", "cogs.events.on_member_update",
              "cogs.utils.dbfunctions"]

modules = []
modules += ["TypingLogs-Typing"]  # Modules for on_typing.py
modules += ["MemberLogs-Nickname", "MemberLogs-Status"]  # Modules for on_member_update.py



class ProLog(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.prefixes = None
        self.config = None
        self.db = None
        self.cogs = cogs
        self.modules = modules
        super().__init__(*args, **kwargs)

    async def __init(self):
        try:
            self.db = await asyncio.wait_for(asyncpg.create_pool(config.postgresql), 10)
        except Exception as e:
            print("Could not conntect not PostGreSQL databse. Exiting", file=sys.stderr)
            return

        self.prefixes = dbfunctions.PrefixesClass(self)
        self.config = dbfunctions.ConfigClass(self)


    async def on_ready(self):
        await self.__init()
        for extension in cogs:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()
        print('=' * 10)
        print(f'Logged in as {self.user} with the id {self.user.id}')
        print("Logged into PostgresSQL server")
        print(f"Loaded cogs {', '.join(self.cogs)}")
        print(f'Guild count: {len(self.guilds)}')
        print('=' * 10)


    async def on_message(self, message):
        if not isinstance(message.channel, discord.TextChannel) or message.author.bot:
            return
        await self.process_commands(message)


    async def get_prefix(self, message):
        try:
            prefixes = await self.prefixes[message.guild.id]
        except KeyError:
            await self.prefixes.setitem(message.guild.id, ['!'])
            prefixes = self.prefixes[str(message.guild.id)]
        except:
            return commands.when_mentioned(self, message)
        return commands.when_mentioned_or(*prefixes)(self, message)



if __name__ == '__main__':
    bot = ProLog(command_prefix=None)
    bot.run(config.token)
