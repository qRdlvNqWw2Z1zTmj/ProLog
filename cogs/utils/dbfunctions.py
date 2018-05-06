import json

import asyncpg
from discord.ext import commands
from discord.ext.commands import TextChannelConverter



class PrefixesClass:
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.con = None 
        self.data = {}  #Local cache for faster data retrieval

    async def __getitem__(self, item: int):
        try:
            res = self.data[str(item)] #Tries to get results from the cache
        except KeyError:
            res = await self.fetch(f'''
            SELECT prefixes FROM Prefixes WHERE GuildID = {item};
            ''') #SQL query to get prefixes for guild
            try:
                res = json.loads(res[0]['prefixes']) #JSON de-serialization
                self.data[str(item)] = res #Caches the result
            except IndexError: #Occurs when the entry for prefixes in guild dont exist
                await self.setitem(item, ['!']) #This sets it to a default value
                return await self.__getitem__(item) #Recursion!
            
        return res

    async def setitem(self, item: int, data): #Was gonna use __setitem__, but await PrefixesClass[something] = blah wont work, only await PrefixesClass.__setitem__
        value = json.dumps(data) #JSON serialization
        try:
            await self.execute(f'''
            INSERT INTO Prefixes (GuildID, prefixes) VALUES ({item}, '{value}');
            ''') 
        except asyncpg.exceptions.UniqueViolationError: #The row already exists
            await self.execute(f'''
            UPDATE Prefixes SET GuildID={item}, prefixes='{value}' WHERE GuildID = {item};
            ''')

        self.data[str(item)] = data #Refreshes the cache
            

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
        self.modules = bot.modules
        self.con = None
        self.data = {} #Local cache for faster data retrieval


    async def __getitem__(self, item: int): #These methods should be nearly equal to methods in PrefixesClass
        try:
            res = self.data[str(item)] # Had to comment this out because for some reason the except didn't work. Remind me to fix/sort/whatever this out
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

    async def set(self, item: int, data): #These methods should be nearly equal to methods in PrefixesClass
        value = json.dumps(data)
        try:
            await self.execute(f'''
            INSERT INTO Configs (GuildID, configs) VALUES ({item}, '{value}');
            ''')
        except asyncpg.exceptions.UniqueViolationError:
            await self.execute(f'''
            UPDATE Configs SET GuildID={item}, configs='{value}' WHERE GuildID = {item};
            ''')
        
        self.data[str(item)] = data
        
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







    # This is gonna be long and broken
    @commands.group()
    async def log(self, ctx):
        """The main logging command."""
        pass

    @log.command()
    async def start(self, ctx, *args):
        """Starts logging specified modules in specified channels.
        It doesn't matter in what order the modules and channels are in, as long as they're correct and separated by spaces it will succeed.
        A list of modules and module catagories can be shown with the command `log show all`."""
        mods = []
        channels = []
        badargs = []

        # Parse the mash of arguments
        for m in args:
            try:
                channel = await TextChannelConverter().convert(ctx, m)
                channels.append(channel)
            except commands.errors.BadArgument:
                if not m.casefold() in map(str.casefold, self.modules):
                    print(f"Bad argument: {m}")
                    badargs.append(m)
                else:
                    mods.append(m)

        # Update the guild configs
        for c in channels:
            for m in mods:
                print(f"Channel: {c.name} {c.id} GuildID: {c.guild.id} Module: {m}")
                await self.togglechannel(c.guild.id, m, c.id)

        # Error on no channels
        if not channels:
            await ctx.send("No channels specified")
            return

        # Error on bad args
        if badargs:
            await ctx.send(f"Invalid argument `{badargs[0]}`. Ignoring" if len(badargs) == 1 else
                           f"Invalid arguments `{', '.join([b for b in badargs])}`. Ignoring" if badargs > 1 else None)

        # Confirmation message
        if mods:
            await ctx.send(f"Started logging modules {', '.join([m for m in mods])} in {', '.join([c.mention for c in channels])}")

def setup(bot):
    bot.add_cog(ConfigClass(bot))






















