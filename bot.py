import asyncio
import json
import sys
import traceback

import asyncpg
import discord
from discord.ext import commands

import config
from cogs.utils import data
from cogs.utils import dbfunctions


class ProLog(commands.Bot):
    def __init__(self):
        self._cogs = data.cogs
        self.modules = data.modules
        async def prefix(bot, message):
            prefixes = await dbfunctions.DatabaseFunctions(self).get_prefixes(bot, message)
            return commands.when_mentioned_or(*prefixes)(bot, message)
        super().__init__(command_prefix=prefix)

    async def _init(self):
        async def init_connection(conn):
            await conn.set_type_codec("jsonb", encoder=json.dumps, decoder=json.loads, schema="pg_catalog")
        try:
            self.db = await asyncio.wait_for(asyncpg.create_pool(config.postgresql, init=init_connection), 10)
        except Exception as e:
            print("Could not conntect not Postgres databse. Exiting", file=sys.stderr)
            print(e)
            await self.logout()

    async def on_ready(self):
        await self._init()

        for extension in data.cogs:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(f"Failed to load extension {extension}.", file=sys.stderr)
                traceback.print_exc()

        print("=" * 10)
        print(f"Logged in as {self.user} with id {self.user.id}")
        print("Logged into PostgresSQL server")
        print(f"Loaded cogs {', '.join(self.cogs)}")
        print(f"Guild count: {len(self.guilds)}")
        print("=" * 10)

    async def on_message(self, message):
        if not isinstance(message.channel, discord.TextChannel) or message.author.bot:
            return
        await self.process_commands(message)


if __name__ == "__main__":
    bot = ProLog()
    bot.run(config.token)


