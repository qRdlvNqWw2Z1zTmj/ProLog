# EXAMPLE FOR PY
# async with self.bot.db.acquire() as connection:
#     # 'connection' is the connection itself
#
#     async with connection.transaction():
#         # this block starts a transaction
#         # if for some reason something raises in this block,
#         # (and isn't caught)
#         # asyncpg will helpfully rollback EVERYTHING that happened in this block
#         # otherwise, it'll just commit as usual when it exits
#
#         my_guilds = await
#         connection.fetch(
#             """
#             SELECT a_cool_column, another_column FROM guilds
#             WHERE id = $1
#             """,  # $1 represents the first var, use $2 and etc for continuing
#             a_guild_id
#         )
#         # my_guilds is a list of Record objects
#         # in this case there should only be one of them
#         # in which case you can use 'fetchrow' instead to just get one anyway
#         a_guild = my_guilds[0]
#
#         # columns can be accessed by index
#         a_cool_column = a_guild[0]  # because it's the first column in the statement
#
#         # or by name
#         another_column = a_guild["another_column"]
#
#         # updates or inserts, etc require execute instead
#         await
#         connection.execute(
#             """
#             INSERT INTO guilds (id)
#             VALUES ($1)
#             ON CONFLICT (id)
#             DO NOTHING
#             """,
#             a_new_guild_id
#         )
#         # this will raise if something fucks up
#         # since we have the transaction we safe tho :ok_hand:
#
#     # exiting the transaction block commits the transaction if nothing went wrong
#
#
# # exiting the acquire block releases the connection back to the pool



class DatabaseFunctions:
    def __init__(self, bot):
        self.bot = bot


    async def get_row(self, dbtable, dbcolumn, guildid: int, key=None):
        # MAKE FULLY SURE NONE OF THESE ARE USER INPUTTED. Constructing queries without the $n format leads to SQLI
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


    async def get_prefixs(self, bot, message):
        prefixes = await self.get_row("configs", "prefixes", message.guild.id, "prefixes")
        return prefixes


    async def get_modules(guildid: int):
        pass


    async def set_item(self, guildid: int, dbtable, dbcolumn, value):
        async with self.bot.db.acquire() as connection:
            async with connection.transaction():
                await connection.execute(f"""
                    UPDATE {dbtable}
                    SET {dbcolumn} = $1
                    WHERE guildid = $2
                """, value, guildid)


    async def remove_item(self, dbtable, dbcolumn, guildid :int, value):
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






















