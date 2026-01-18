"""Async HyperX client - main entry point for async SDK usage."""

from __future__ import annotations

from typing import TYPE_CHECKING

from hyperx.http import DEFAULT_BASE_URL, AsyncHTTPClient
from hyperx.resources.async_batch import AsyncBatchAPI
from hyperx.resources.async_entities import AsyncEntitiesAPI
from hyperx.resources.async_hyperedges import AsyncHyperedgesAPI
from hyperx.resources.async_paths import AsyncPathsAPI
from hyperx.resources.async_search import AsyncSearchAPI

if TYPE_CHECKING:
    from hyperx.cache.base import Cache


class AsyncHyperX:
    """Async HyperX client for interacting with the HyperX API.

    Use this client for async/await code patterns in asyncio applications.
    For synchronous code, use the regular HyperX client instead.

    Example:
        >>> from hyperx import AsyncHyperX
        >>> async with AsyncHyperX(api_key="hx_sk_...") as db:
        ...     entity = await db.entities.create(name="React", entity_type="concept")
        ...     paths = await db.paths.find("e:...", "e:...")

        >>> # With caching
        >>> from hyperx.cache import InMemoryCache
        >>> cache = InMemoryCache(max_size=100, ttl=300)
        >>> async with AsyncHyperX(api_key="hx_sk_...", cache=cache) as db:
        ...     # Repeated path queries will use cache
        ...     paths = await db.paths.find("e:start", "e:end")
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
        *,
        cache: Cache | None = None,
        server_cache: bool = False,
    ):
        """Initialize AsyncHyperX client.

        Args:
            api_key: Your HyperX API key (starts with hx_sk_)
            base_url: API base URL (default: https://api.hyperxdb.dev)
            timeout: Request timeout in seconds (default: 30)
            cache: Optional cache backend for client-side caching of expensive
                   operations like path queries and searches.
            server_cache: Enable server-side cache hints. When True, the server
                          may cache results for improved performance.
        """
        if not api_key.startswith("hx_sk_"):
            raise ValueError("API key must start with 'hx_sk_'")

        self._http = AsyncHTTPClient(api_key, base_url, timeout)
        self._cache = cache
        self._server_cache = server_cache

        self.entities = AsyncEntitiesAPI(self._http)
        self.hyperedges = AsyncHyperedgesAPI(self._http)
        self.paths = AsyncPathsAPI(self._http, cache=cache)
        self.search = AsyncSearchAPI(self._http, cache=cache)
        self.batch = AsyncBatchAPI(self._http)

    async def close(self) -> None:
        """Close the client and release resources."""
        await self._http.close()

    async def __aenter__(self) -> "AsyncHyperX":
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
