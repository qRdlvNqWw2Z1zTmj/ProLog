import asyncio
import json
import sys
import traceback

import asyncpg
import discord
from discord.ext import commands

import config
from cogs.utils import dbfunctions

cogs = ["cogs.help", "cogs.dev", "cogs.eval", "cogs.general", "cogs.errorhandler", "cogs.guildevents", "cogs.events.on_typing", "cogs.events.on_member_update", "cogs.utils.dbfunctions", "cogs.dbcommands", "cogs.utils.dbfunctions"]

modules = []
modules += ["TypingLogs-Typing"]  # Modules for on_typing.py
modules += ["MemberLogs-Nickname", "MemberLogs-Status"]  # Modules for on_member_update.py



class ProLog(commands.Bot):
    def __init__(self):
        self._cogs = cogs
        self.modules = modules
        self._prefix_cog = None
        async def prefix(bot, message):
            if self._prefix_cog is None:
                self._prefix_cog = self.get_cog('DatabaseFunctions')
                try:
                    return await prefix(bot, message) #Recursion!
                except RecursionError:
                    print('Prefix stuff broken')
                    exit()
            prefixes = await self._prefix_cog.get_prefixes(bot, message)
            return commands.when_mentioned_or(*prefixes)(bot, message)
        super().__init__(command_prefix=prefix)

    async def __init(self):
        try:
            self.db = await asyncio.wait_for(asyncpg.create_pool(config.postgresql), 10)
            conn = conn = await asyncpg.connect(config.postgresql)
            await conn.set_type_codec(
                'jsonb',
                encoder=json.dumps,
                decoder=json.loads,
                schema='pg_catalog')
        except Exception as e:
            print("Could not conntect not PostGreSQL databse. Exiting", file=sys.stderr)
            print(e)
            quit()
        finally:
            await conn.close()

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


if __name__ == '__main__':
    bot = ProLog()
    bot.run(config.token)
