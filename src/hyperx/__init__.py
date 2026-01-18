"""HyperX Python SDK - The knowledge layer for AI."""

from hyperx._version import __version__
from hyperx.async_client import AsyncHyperX
from hyperx.batch import (
    BatchItemResult,
    BatchResult,
    EntityCreate,
    EntityDelete,
    HyperedgeCreate,
    HyperedgeDelete,
)
from hyperx.client import HyperX
from hyperx.exceptions import (
    AuthenticationError,
    HyperXError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from hyperx.models import Entity, Hyperedge, HyperedgeMember, PathResult, SearchResult
from hyperx.query import AsyncQueryExecutor, Query, QueryExecutor, RoleFilter
from hyperx.resources.hyperedges import MemberInput

__all__ = [
    "HyperX",
    "AsyncHyperX",
    "Entity",
    "Hyperedge",
    "HyperedgeMember",
    "MemberInput",
    "SearchResult",
    "PathResult",
    "HyperXError",
    "AuthenticationError",
    "NotFoundError",
    "ValidationError",
    "RateLimitError",
    "ServerError",
    # Batch operation models
    "BatchItemResult",
    "BatchResult",
    "EntityCreate",
    "EntityDelete",
    "HyperedgeCreate",
    "HyperedgeDelete",
    # Query builder
    "Query",
    "QueryExecutor",
    "AsyncQueryExecutor",
    "RoleFilter",
]


# Lazy imports for optional integrations
def __getattr__(name: str):
    if name == "integrations":
        from hyperx import integrations
        return integrations
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
