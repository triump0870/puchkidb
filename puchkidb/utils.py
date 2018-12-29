"""
Utility functions.
"""

import warnings
from collections import OrderedDict
from contextlib import contextmanager

# Python 2/3 independant dict iteration
iteritems = getattr(dict, 'iteritems', dict.items)
itervalues = getattr(dict, 'itervalues', dict.values)


class LRUCache:
    # @param capacity, an integer
    def __init__(self, capacity=None):
        self.capacity = capacity
        self.__cache = OrderedDict()

    @property
    def lru(self):
        return list(self.__cache.keys())

    @property
    def length(self):
        return len(self.__cache)

    def clear(self):
        self.__cache.clear()

    def __len__(self):
        return self.length

    def __contains__(self, item):
        return item in self.__cache

    def __setitem__(self, key, value):
        self.set(key, value)

    def __delitem__(self, key):
        del self.__cache[key]

    def __getitem__(self, key):
        return self.get(key)

    def get(self, key, default=None):
        value = self.__cache.get(key)
        if value:
            del self.__cache[key]
            self.__cache[key] = value
            return value
        return default

    def set(self, key, value):
        if self.__cache.get(key):
            del self.__cache[key]
            self.__cache[key] = value
        else:
            self.__cache[key] = value
            # Check, if the cache is full and we have to remove old items
            # If the queue is of unlimited size, self.capacity is NaN and
            # x > NaN is always False in Python and the cache won't be cleared.
            if self.capacity is not None and self.length > self.capacity:
                self.__cache.popitem(last=False)
