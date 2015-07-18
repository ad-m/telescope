from onion_py.caching import OnionCache, key_serializer
from django.core.cache import cache


class OnionDjangoCache(OnionCache):
    def __init__(self):
        self.cache = cache

    def get(self, query, params):
        return self.cache.get(key_serializer(query, params))

    def set(self, query, params, document):
        return self.cache.set(key_serializer(query, params), document)
