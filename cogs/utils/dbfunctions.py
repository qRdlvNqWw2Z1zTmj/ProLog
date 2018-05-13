from .cache import LFUCache as lfucache

class DatabaseFunctions:
    def __init__(self, bot):
        self.bot = bot
        self.cache = lfucache(limit = 10) #Icrease this when we go big

    async def get_row(self,  guildid: int, dbtable, dbcolumn, key=None):
        result = await self.bot.db.fetchrow(f"""
            SELECT {dbcolumn} FROM {dbtable} 
            WHERE guildid = $1
            """, guildid)
        if result is None:
            async with self.bot.db.acquire() as connection:
                async with connection.transaction():
                    await connection.execute(f"""
                      INSERT INTO configs(guildid, prefixes)
                      VALUES ($1, $2)
                  """, guildid, ["!"])
        if key is not None:
            result = result[key]
        return result

    async def get_prefixes(self, bot, message):
        try:
            return self.cache[message]
        except KeyError:
            res = await self.get_row(message.guild.id, "configs", "prefixes", "prefixes")
            self.cache[message] = res
            return await self.get_prefixes(bot, message)
        
    async def set_prefix(self, guildid: int, value):
        self.cache[guildid] = value
        await self.set_item(guildid, "configs", "prefixes", value)
        
    async def get_modules(self, guildid: int):
        pass
    
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
    bot.add_cog(DatabaseFunctions(bot))
#whitespace
