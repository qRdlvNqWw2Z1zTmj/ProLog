from discord.ext import commands
from .cache import cached_function

class DatabaseFunctions:
    def __init__(self, bot):
        self.bot = bot
        self.get_prefixes.instance = self
        bot.loop.create_task(self.init_cache())

    async def init_cache(self):
        await self.bot.wait_until_ready()
        self.get_prefixes.limit = len(self.bot.guilds) / 2

    @cached_function()
    async def get_prefixes(self, message):
        prefixes = await self.fetch_value(message.guild.id, "configs", "prefixes")
        if prefixes is None:
            await self.bot.db.execute("INSERT INTO configs(guildid, prefixes) VALUES($1, '{!}')", message.guild.id)
            self.get_prefixes.invalidate(self.get_prefixes.get_id(self.bot, message))
            prefixes = await self.fetch_value(message.guild.id, "configs", "prefixes")
        return commands.when_mentioned_or(*prefixes)(self.bot, message)

    async def fetch_row(self, guildid, dbtable):
        result = await self.bot.db.fetchrow(f"""
            SELECT * FROM {dbtable} 
            WHERE guildid = $1
            """, guildid)
        return result

    async def fetch_value(self, guildid, dbtable, dbcolumn):
        result = await self.bot.db.fetchval(f"""
        SELECT {dbcolumn} FROM {dbtable}
        WHERE guildid = $1
        """, guildid)
        return result

    async def set_item(self, guildid: int, dbtable, dbcolumn, value):
        if dbcolumn.lower() == 'prefixes':
            self.get_prefixes.invalidate_cache()
        async with self.bot.db.acquire() as connection:
            async with connection.transaction():
                await connection.execute(f"""
                    UPDATE {dbtable}
                    SET {dbcolumn} = $1
                    WHERE guildid = $2
                """, value, guildid)

    async def remove_item(self, guildid: int, dbtable, dbcolumn, value):
        if dbcolumn.lower() == 'prefixes':
            self.get_prefixes.invalidate_cache()
        async with self.bot.db.acquire() as connection:  # Is a transaction really necessary?
            async with connection.transaction():
                row = await self.get_row(dbtable, dbcolumn, guildid)
                row.pop(value)
                await connection.execute(f"""
                    UPDATE {dbtable}
                    SET {dbcolumn} = $1
                    WHERE guildid = $2
                """, row, guildid)
