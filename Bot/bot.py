import asyncio
import sys
import traceback
import json
import asyncpg
import discord
from discord.ext import commands

import config
from cogs.utils import data
from cogs.utils.functions import get_prefixes


class ProLog(commands.Bot):
    extensions = {}
    config = config
    def __init__(self):
        self.modules = data.modules
        self.functions = functions.Functions(self)
        super().__init__(command_prefix=get_prefixes)

    async def on_ready(self):
        for extension in data.cogs:
            try:
                self.load_extension(extension)
            except Exception:
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


    async def on_member_remove(self, member):
        bans = await member.guild.bans()
        users = [c.user for c in bans]
        user = self.get_user(member.id)

        async for entry in member.guild.audit_logs(limit=1):
            if entry.action != discord.AuditLogAction.kick:
                return
                
            if entry.target == user:
                f = None
                for c in member.guild.channels:
                    p = c.permissions_for(member.guild.me)
                    if p.create_instant_invite:
                        if isinstance(c, discord.TextChannel):
                            f = c
                            break

                if f is not None:
                    self.dispatch('member_kick', member, entry)
                    r = "This is an action that lets the bot differentiate between member kick and member leave."
                    inv = await f.create_invite(reason=r)
                    await inv.delete(reason=r)
                    return

        self.dispatch('member_leave', member)




if __name__ == "__main__":
    bot = ProLog()
    bot.run(config.token)
