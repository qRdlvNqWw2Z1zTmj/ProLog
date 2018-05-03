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
            try:
                res = json.loads(res[0]['prefixes'])
                self.data[str(item)] = res
            except IndexError:
                await self.setitem(item, ['!'])
                return await self.__getitem__(item)
            
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
            self.con = None

        
            

class ConfigClass:
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
            SELECT configs FROM Configs WHERE GuildID = {item};
            ''')
            try:
                res = json.loads(res[0]['configs'])
                self.data[str(item)] = res
            except IndexError:
                await self.set(item, {})
                return await self.__getitem__(item)
        return res

    async def set(self, item: int, value):
        value = json.dumps(value)
        try:
            await self.execute(f'''
            INSERT INTO Configs (GuildID, configs) VALUES ({item}, '{value}');
            ''')
        except asyncpg.exceptions.UniqueViolationError:
            await self.execute(f'''
            UPDATE Configs SET GuildID={item}, configs='{value}' WHERE GuildID = {item};
            ''')
        try:
            del self.data[str(item)]
        except KeyError: pass
        
    async def togglechannel(self, GuildID: int, type: str, ChannelID: int):
        config = await self[GuildID]
        channels = config.get(type)
        if channels is None: channels = []
        if ChannelID not in channels:
            new = channels + [ChannelID]
            config[type] = new
            await self.set(GuildID, config)
            return True
        else:
            new = channels.remove(ChannelID)
            config[type] = new
            await self.set(GuildID, config)
            return False


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
            self.con = None
