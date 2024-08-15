#!/usr/bin/python3
""" FIFO Caching """

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ FIFOCache caching system """

    def __init__(self):
        """ Initialize the cache """
        super().__init__()

    def put(self, key, item):
        """ Add an item in the cache """
        if key is None or item is None:
            return

        if (len(self.cache_data) >= BaseCaching.MAX_ITEMS and
                key not in self.cache_data):
            first_key = next(iter(self.cache_data))
            del self.cache_data[first_key]
            print("DISCARD:", first_key)

        self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key """
        if key is None:
            return None
        return self.cache_data.get(key, None)
