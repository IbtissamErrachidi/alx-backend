#!/usr/bin/python3
""" MRU Caching """

from base_caching import BaseCaching
from collections import OrderedDict


class MRUCache(BaseCaching):
    """ MRUCache caching system """

    def __init__(self):
        """ Initialize the cache """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """ Add an item in the cache """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data.move_to_end(key)
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            discarded_key, _ = self.cache_data.popitem(last=True)
            print(f"DISCARD: {discarded_key}")

        self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key """
        if key is None or key not in self.cache_data:
            return None

        self.cache_data.move_to_end(key)
        return self.cache_data[key]
