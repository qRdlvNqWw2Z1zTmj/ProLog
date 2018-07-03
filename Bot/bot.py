import asyncio
import json
import sys
import traceback

import asyncpg
import discord
from discord.ext import commands
from cogs.utils import functions
import config
from cogs.utils import data


class ProLog(commands.Bot):
    def __init__(self):
        self.modules = data.modules
        super().__init__(command_prefix=functions.Functions(self).get_prefixes)

    async def on_ready(self):
        async def init_connection(conn):
            await conn.set_type_codec("jsonb", encoder=json.dumps, decoder=json.loads, schema="pg_catalog")

        try:
            self.db = await asyncio.wait_for(asyncpg.create_pool(config.postgresql, init=init_connection), 10)
        except Exception as e:
            print(f"Could not connect not Postgres database. Exiting", file=sys.stderr)
            traceback.print_exc()
            await self.logout()

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


