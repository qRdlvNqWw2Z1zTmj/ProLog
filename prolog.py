import traceback

import discord
from discord.ext import commands

from cogs.utils import data


class ProLog(commands.Bot):
    async def on_ready(self):
        for extension in data.cogs:
            try:
                self.load_extension(extension)
            except Exception:
                print(f"Failed to load extension {extension}")
                traceback.print_exc()

        print("=" * 10)
        print(f"Logged in as {self.user} with id {self.user.id}")
        print("Logged into PostgresSQL server" if self.db is not None else None)
        print(f"Loaded cogs {', '.join(self.cogs)}")
        print(f"Guild count: {len(self.guilds)}")
        print("=" * 10)

    async def on_message(self, message):
        if not isinstance(message.channel, discord.TextChannel) or message.author.bot:
            return
        await self.process_commands(message)
