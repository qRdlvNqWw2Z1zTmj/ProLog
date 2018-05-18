import asyncio
import inspect
from functools import wraps

class LFUNode:

    __slots__ = ('key', 'value', 'freqnode', 'previous', 'next')

    def __init__(self, key, value, freqnode, previous, next_):
        self.key = key
        self.value = value
        self.freqnode = freqnode

        self.previous = previous
        self.next = next_

    def free_myself(self):
        if self.freqnode.cache_head == self.freqnode.cache_tail:
            self.freqnode.cache_head = self.freqnode.cache_tail = None
        elif self.freqnode.cache_head == self:
            self.next.previous = None
            self.freqnode.cache_head = self.next
        elif self.freqnode.cache_tail == self:
            self.previous.next = None
            self.freqnode.cache_tail = self.previous
        else:
            self.previous.next = self.next
            self.next.previous = self.previous

        self.previous = None
        self.next = None
        self.freqnode = None


class FreqNode:

    __slots__ = ('freq', 'previous', 'next', 'cache_head', 'cache_tail')

    def __init__(self, freq, previous, next_):
        self.freq = freq
        self.previous = previous
        self.next = next_

        self.cache_head = None
        self.cache_tail = None

    def count_caches(self):
        if self.cache_head is None and self.cache_tail is None:
            return 0
        elif self.cache_head == self.cache_tail:
            return 1
        else:
            return '2+'

    def remove(self):
        if self.previous is not None:
            self.previous.next = self.next
        if self.next is not None:
            self.next.previous = self.previous

        previous = self.previous
        next_ = self.next
        self.previous = self.next = self.cache_head = self.cache_tail = None

        return previous, next_

    def pop_head_cache(self):
        if self.cache_head is None and self.cache_tail is None:
            return None
        elif self.cache_head == self.cache_tail:
            cache_head = self.cache_head
            self.cache_head = self.cache_tail = None
            return cache_head
        else:
            cache_head = self.cache_head
            self.cache_head.next.previous = None
            self.cache_head = self.cache_head.next
            return cache_head

    def append_cache_to_tail(self, cache_node):
        cache_node.freqnode = self

        if self.cache_head is None and self.cache_tail is None:
            self.cache_head = self.cache_tail = cache_node
        else:
            cache_node.previous = self.cache_tail
            cache_node.next = None
            self.cache_tail.next = cache_node
            self.cache_tail = cache_node

    def insert_after_me(self, freq_node):
        freq_node.previous = self
        freq_node.next = self.next

        if self.next is not None:
            self.next.previous = freq_node

        self.next = freq_node

    def insert_before_me(self, freq_node):
        if self.previous is not None:
            self.previous.next = freq_node

        freq_node.previous = self.previous
        freq_node.next = self
        self.previous = freq_node


class LFUCache(object):

    __slots__ = ('cache', 'limit', 'freq_link_head')

    def __init__(self, limit=1000):
        self.cache = {}
        if limit > 0:
            self.limit = limit 
        else:
            raise ValueError('Limit must be more than 0')
        self.freq_link_head = None

    def __len__(self):
        return len(self.cache)

    def __repr__(self):
        return f'<LFU CACHE(LIMIT: {self.limit} ENTRIES: {len(self)})>'

    def __str__(self):
        return f'Items({[(k, v.value) for k, v in self.cache.items()]})'

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        return self.set(key=key, value=value)

    def __delitem__(self, key):
        lfunode = self.cache[key]
        lfunode.free_myself()

        del self.cache[key]

    def __contains__(self, item):
        return item in self.cache

    def get(self, key):
        if key in self.cache:
            cache_node = self.cache[key]
            freqnode = cache_node.freqnode
            value = cache_node.value

            self.move_forward(cache_node, freqnode)

            return value
        else:
            raise KeyError(f'{key} not in cache')

    def set(self, key, value):

        if key not in self.cache:
            if len(self.cache) >= self.limit:
                self.dump_cache()

            self.create_cache(key, value)
        else:
            cache_node = self.cache[key]
            freq_node = cache_node.freqnode
            cache_node.value = value

            self.move_forward(cache_node, freq_node)

    def move_forward(self, cache_node, freqnode):
        if freqnode.next is None or freqnode.next.freq != freqnode.freq + 1:
            target_freq_node = FreqNode(freqnode.freq + 1, None, None)
            target_empty = True
        else:
            target_freq_node = freqnode.next
            target_empty = False

        cache_node.free_myself()
        target_freq_node.append_cache_to_tail(cache_node)

        if target_empty:
            freqnode.insert_after_me(target_freq_node)

        if freqnode.count_caches() == 0:
            if self.freq_link_head == freqnode:
                self.freq_link_head = target_freq_node

            freqnode.remove()

    def dump_cache(self):
        head_freq_node = self.freq_link_head
        self.cache.pop(head_freq_node.cache_head.key)
        head_freq_node.pop_head_cache()

        if head_freq_node.count_caches() == 0:
            self.freq_link_head = head_freq_node.next
            head_freq_node.remove()

    def create_cache(self, key, value):
        cache_node = LFUNode(key, value, None, None, None)
        self.cache[key] = cache_node

        if self.freq_link_head is None or self.freq_link_head.freq != 0:
            new_freq_node = FreqNode(0, None, None)
            new_freq_node.append_cache_to_tail(cache_node)

            if self.freq_link_head is not None:
                self.freq_link_head.insert_before_me(new_freq_node)

            self.freq_link_head = new_freq_node
        else:
            self.freq_link_head.append_cache_to_tail(cache_node)

class CachedFunction:
    def __init__(self, func, limit=1000):
        self.limit = limit
        self.cache = LFUCache(limit=self.limit)
        self.func = func

    def __call__(self, *args, **kwargs):
            id = hash(str(args)+str(kwargs))
            try:
                return self.cache[id]
            except KeyError:
                res = self.func(*args, **kwargs)
                self.cache[id] = res
                return res

    def get_id(self, *args, **kwargs): 
        return hash(str(args)+str(kwargs))

    def invalidate(self, id):
        try:
            del self.cache[id]
        except KeyError: pass

    def invalidate_cache(self):
        self.cache = LFUCache(limit=self.limit)

class AsyncCachedFunction(CachedFunction):
    async def __call__(self, *args, **kwargs):
        id = hash(str(args)+str(kwargs))
        try:
            return self.cache[id]
        except KeyError:
            res = await self.func(*args, **kwargs)
            self.cache[id] = res
            return res

def cached_function(limit: int=1000):
    def dec(fn):
        if asyncio.iscoroutinefunction(fn): 
            class Wrap(AsyncCachedFuncion):
                @wraps(fn)
                async def __call__(self, *args, **kwargs):
                    await super().__call__(*args, **kwargs) 
            




        else: 

            class Wrap(CachedFuncion):
                @wraps(fn)
                def __call__(self, *args, **kwargs):
                    super().__call__(*args, **kwargs) 




        return Wrap(fn, limit=limit) 
    return dec
