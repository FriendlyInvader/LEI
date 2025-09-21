import time

class dict_cache:
    _cache = {}
    _window = 3.0 # seconds

    def __init__(self, get_value, window:float):
        self._cache = {}
        self._get_value = get_value
        self._window = window

    def get(self, key):
        if key in self._cache:
            value = self._cache[key]
            diff = time.time() - value[0]
            if diff < self._window:
                return value[1]
            else: # invalidate cache
                del self._cache[key]
        value = (time.time(), self._get_value(key))
        self._cache[key] = value
        return value[1]
