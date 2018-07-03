import asyncio
import json
import sys
import traceback
import asyncio

import asyncpg
import discord
from discord.ext import commands
from cogs.utils import functions
import config
from cogs.utils import data


class ProLog(commands.Bot):
    extensions = {}
    config = config
    def __init__(self):
        self.modules = data.modules
        
        super().__init__(command_prefix="!")

    async def on_ready(self):
        self.load_extension("cogs.utils.functions")
        await asyncio.sleep(10)
        self.command_prefix = self.dbfuncs.get_prefixes
        bot.db = bot.db.result()

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


