import asyncio
import json
import sys
import traceback

import asyncpg
from discord.ext import commands

from cogs.utils.cache import cached_function




class Functions:
    def __init__(self, bot):
        self.bot = bot

    async def completed(self, message):
        await message.add_reaction(":check:444926155800444949")

    async def not_completed(self, message):
        await message.add_reaction("negative:444926170895613962")

    def escape(self, cont):
        for c in cont:
            cont.replace(c, f'\{c}')
        return cont

    async def get_row(self,  guildid: int, dbtable, dbcolumn, key=None):
        result = await self.bot.db.fetchrow(f"""
            SELECT {dbcolumn} FROM {dbtable} 
            WHERE guildid = $1
            """, guildid)
        if result is None:
            async with self.bot.db.acquire() as connection:
                async with connection.transaction():
                    await connection.execute("""
                      INSERT INTO configs(guildid, prefixes)
                      VALUES ($1, $2)
                  """, guildid, ["!"])
        if key is not None:
            try:
                result = result[key]
            except TypeError:
                if dbcolumn == "prefixes" and result is None:
                    return "!"
                return None
        return result

    @cached_function()
    async def get_prefixes(self, bot, message):
        if self.bot.db is None:
            dbprefixes = ['!']
        else:
            dbprefixes = await self.get_row(message.guild.id, "configs", "prefixes", "prefixes")
        return commands.when_mentioned_or(*dbprefixes)(bot, message)


    async def set_prefix(self, message, value):
        self.get_prefixes.invalidate(self.get_prefixes.get_id(self.bot, message))
        await self.set_item(message.guild.id, "configs", "prefixes", value)


    async def set_item(self, guildid: int, dbtable, dbcolumn, value):
        async with self.bot.db.acquire() as connection:
            async with connection.transaction():
                await connection.execute(f"""
                    UPDATE {dbtable}
                    SET {dbcolumn} = $1
                    WHERE guildid = $2
                """, value, guildid)


    async def remove_item(self, guildid :int, dbtable, dbcolumn, value):
        async with self.bot.db.acquire() as connection:
            async with connection.transaction():
                row = await self.get_row(dbtable, dbcolumn, guildid)
                row.pop(value)
                await connection.execute(f"""
                    UPDATE {dbtable}
                    SET {dbcolumn} = $1
                    WHERE guildid = $2
                """, row, guildid)

def setup(bot):
    async def init_connection(conn):
            await conn.set_type_codec("jsonb", encoder=json.dumps, decoder=json.loads, schema="pg_catalog")

    async def init(bot):
        try:
            bot.dbfuncs = Functions(bot)
            bot.command_prefix = bot.dbfuncs.get_prefixes
            bot.db = await asyncio.wait_for(asyncpg.create_pool(bot.config.postgresql, init=init_connection), 10)
        except Exception as e:
            print(f"Could not connect not Postgres database", file=sys.stderr)
            traceback.print_exc()
            print()


    bot.loop.create_task(init(bot))

def teardown(bot):
    bot.loop.create_task(bot.db.close())
    bot.db = None
    bot.command_prefix = commands.when_mentioned_or(['!'])

