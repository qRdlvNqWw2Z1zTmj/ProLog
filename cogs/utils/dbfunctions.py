import asyncpg
import json

class PrefixesClass:
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.con = None
        self.data = {}

    async def __getitem__(self, item: int):
        try:
            res = self.data[str(item)]
        except KeyError:
            res = await self.fetch(f'''
            SELECT prefixes FROM Prefixes WHERE GuildID = {item};
            ''')
            res = json.loads(res[0]['prefixes'])
            self.data[str(item)] = res
        return res

    async def setitem(self, item: int, value): #Was gonna use __setitem__ ,but await PrefixesClass[something] = blah wont work, only await PrefixesClass.__setitem__
        value = json.dumps(value)
        try:
            await self.execute(f'''
            INSERT INTO Prefixes (GuildID, prefixes) VALUES ({item}, '{value}');
            ''')
        except asyncpg.exceptions.UniqueViolationError:
            await self.execute(f'''
            UPDATE Prefixes SET GuildID={item}, prefixes='{value}' WHERE GuildID = {item};
            ''')
        try:
            del self.data[str(item)]
        except KeyError: pass
            

    async def create_con(self):
        self.con = await self.db.acquire()

    async def verify_con(self):
        if self.con is None:
            await self.create_con()
            return await self.verify_con()
        return True

    async def execute(self, query: str, *args, timeout: float=None):
        if await self.verify_con():
            return await self.con.execute(query, *args, timeout=timeout)

    async def fetch(self, query, *args, timeout=None):
        if await self.verify_con():
            return await self.con.fetch(query, *args, timeout=timeout)

    async def close(self):
        if await self.verify_con():
            await self.con.close()

        
            

class ConfigClass:
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.con = None
        self.data = {}

    async def create_con(self):
        self.con = await self.db.acquire()

    async def verify_con(self):
        if self.con is None:
            await self.create_con()
            return await self.verify_con()
        return True

    async def execute(self, query: str, *args, timeout: float=None):
        if await self.verify_con():
            return await self.con.execute(query, *args, timeout=timeout)

    async def fetch(self, query, *args, timeout=None):
        if await self.verify_con():
            return await self.con.fetch(query, *args, timeout=timeout)

    async def close(self):
        if await self.verify_con():
            await self.con.close()
