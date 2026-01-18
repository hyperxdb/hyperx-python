"""Cache package for HyperX SDK.

This package provides caching functionality with a protocol-based design
allowing for different cache backend implementations.

Example:
    >>> from hyperx.cache import Cache, InMemoryCache
    >>> cache = InMemoryCache(max_size=100, ttl=60)
    >>> cache.set("key", {"data": 123})
    >>> cache.get("key")
    {'data': 123}
    >>> isinstance(cache, Cache)
    True
"""

from hyperx.cache.base import Cache
from hyperx.cache.memory import InMemoryCache

__all__ = ["Cache", "InMemoryCache"]
