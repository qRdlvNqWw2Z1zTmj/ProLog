from discord.ext import commands

from cogs.utils.cache import cached_function


class DatabaseFunctions:
    def __init__(self, bot):
        self.bot = bot

    async def get_row(self, guildid: int, dbtable, dbcolumn, key=None):
        result = await self.bot.db.fetchrow(f"""
            SELECT {dbcolumn} FROM {dbtable} 
            WHERE guildid = $1
            """, guildid)
        if key is not None:
            try:
                return result[key]
            except:
                return result
        return result

    @cached_function()
    async def get_prefixes(self, bot, message):
        prefixes = await self.get_row(message.guild.id, "configs", "prefixes", "prefixes")
        print(prefixes)
        if prefixes is None:
            print("Set")
            await self.set_item(message.guild.id, "configs", "prefixes", ['!'])
            self.get_prefixes.invalidate(self.get_prefixes.get_id(self.bot, message))
        print(f"Prefixes: {prefixes}, {prefixes}")
        return commands.when_mentioned_or(*prefixes)(bot, message)

    async def set_item(self, guildid: int, dbtable, dbcolumn, value):
        async with self.bot.db.acquire() as connection:
            async with connection.transaction():
                await connection.execute(f"""
                    UPDATE {dbtable}
                    SET {dbcolumn} = $1
                    WHERE guildid = $2
                """, value, guildid)

    async def remove_item(self, guildid: int, dbtable, dbcolumn, value):
        async with self.bot.db.acquire() as connection:
            async with connection.transaction():
                row = await self.get_row(dbtable, dbcolumn, guildid)
                row.pop(value)
                await connection.execute(f"""
                    UPDATE {dbtable}
                    SET {dbcolumn} = $1
                    WHERE guildid = $2
                """, row, guildid)
