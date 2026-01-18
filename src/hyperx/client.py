"""HyperX client - main entry point for the SDK."""

from __future__ import annotations

from typing import TYPE_CHECKING

from hyperx.http import DEFAULT_BASE_URL, HTTPClient
from hyperx.resources.batch import BatchAPI
from hyperx.resources.entities import EntitiesAPI
from hyperx.resources.hyperedges import HyperedgesAPI
from hyperx.resources.paths import PathsAPI
from hyperx.resources.search import SearchAPI
from hyperx.resources.webhooks import WebhooksAPI

if TYPE_CHECKING:
    from hyperx.cache.base import Cache
    from hyperx.query import Query, QueryExecutor


class HyperX:
    """HyperX client for interacting with the HyperX API.

    Example:
        >>> from hyperx import HyperX
        >>> db = HyperX(api_key="hx_sk_...")
        >>> entity = db.entities.create(name="React", entity_type="concept")
        >>> edge = db.hyperedges.create(
        ...     description="React provides Hooks",
        ...     members=[
        ...         {"entity_id": entity.id, "role": "subject"},
        ...         {"entity_id": "e:hooks", "role": "object"},
        ...     ]
        ... )

        >>> # With caching
        >>> from hyperx.cache import InMemoryCache
        >>> cache = InMemoryCache(max_size=100, ttl=300)
        >>> db = HyperX(api_key="hx_sk_...", cache=cache)
        >>> # Repeated path queries will use cache
        >>> paths = db.paths.find("e:start", "e:end")
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
        """Initialize HyperX client.

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

        self._http = HTTPClient(api_key, base_url, timeout)
        self._cache = cache
        self._server_cache = server_cache

        self.entities = EntitiesAPI(self._http)
        self.hyperedges = HyperedgesAPI(self._http)
        self.paths = PathsAPI(self._http, cache=cache)
        self.search = SearchAPI(self._http, cache=cache)
        self.batch = BatchAPI(self._http)
        self.webhooks = WebhooksAPI(self._http)

    def query(self, query: Query) -> QueryExecutor:
        """Create query executor for fluent queries.

        Build complex queries with role-based filtering using the Query builder,
        then execute them with the returned QueryExecutor.

        Args:
            query: A Query object built with the fluent Query builder

        Returns:
            QueryExecutor that can be used to execute the query

        Example:
            >>> from hyperx.query import Query
            >>> q = Query().where(role="subject", entity="e:react").limit(10)
            >>> results = db.query(q).execute()
        """
        from hyperx.query import QueryExecutor

        return QueryExecutor(self._http, query)

    def close(self) -> None:
        """Close the client and release resources."""
        self._http.close()

    def __enter__(self) -> "HyperX":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
