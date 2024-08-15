#!/usr/bin/python3
""" LFU Caching """

from base_caching import BaseCaching
from collections import OrderedDict


class LFUCache(BaseCaching):
    """ LFUCache caching system """

    def __init__(self):
        """ Initialize the cache """
        super().__init__()
        self.freq = {}
        self.order = OrderedDict()

    def put(self, key, item):
        """ Add an item in the cache """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self.freq[key] += 1
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                min_freq = min(self.freq.values())
                least_freq_keys = [
                    k for k, v in self.freq.items() if v == min_freq
                ]
                lru_key = min(least_freq_keys, key=lambda k: self.order[k])
                del self.cache_data[lru_key]
                del self.freq[lru_key]
                del self.order[lru_key]
                print(f"DISCARD: {lru_key}")

            self.cache_data[key] = item
            self.freq[key] = 1
            self.order[key] = len(self.order)  # Update order

    def get(self, key):
        """ Get an item by key """
        if key is None or key not in self.cache_data:
            return None
        self.freq[key] += 1
        self.order[key] = len(self.order)
        return self.cache_data[key]
