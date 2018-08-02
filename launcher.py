import asyncio
import json
import traceback

import asyncpg

import config
from cogs.utils import data
from cogs.utils.database import DatabaseFunctions
from prolog import ProLog

try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def run_bot():
    loop = asyncio.get_event_loop()

    async def init_connection(conn):
        await conn.set_type_codec("jsonb", encoder=json.dumps, decoder=json.loads, schema="pg_catalog")

    try:
        pool = loop.run_until_complete(asyncpg.create_pool(config.postgresql, init=init_connection))
    except Exception:
        print(f"Could not connect not Postgres database. Exiting")
        traceback.print_exc()
        return

    bot = ProLog(command_prefix=None)

    bot.modules = data.modules
    bot.db = pool
    bot.command_prefix = DatabaseFunctions(bot).get_prefixes

    bot.run(config.token)


if __name__ == "__main__":
    run_bot()
