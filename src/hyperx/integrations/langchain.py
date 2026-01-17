"""LangChain integration for HyperX.

Install: pip install hyperx[langchain]

Example:
    >>> from hyperx import HyperX
    >>> from hyperx.integrations.langchain import HyperXRetriever
    >>>
    >>> db = HyperX(api_key="hx_sk_...")
    >>> retriever = HyperXRetriever(client=db, strategy="search", k=10)
    >>> docs = retriever.invoke("React state management")
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import ConfigDict

try:
    from langchain_core.callbacks import CallbackManagerForRetrieverRun
    from langchain_core.documents import Document
    from langchain_core.retrievers import BaseRetriever
except ImportError as e:
    raise ImportError(
        "LangChain integration requires langchain-core. "
        "Install with: pip install hyperx[langchain]"
    ) from e

if TYPE_CHECKING:
    from hyperx import AsyncHyperX, HyperX

__all__ = ["HyperXRetriever", "HyperXRetrievalPipeline"]


class HyperXRetriever(BaseRetriever):
    """LangChain retriever backed by HyperX hypergraph database.

    Two strategies available:
    - "search": Simple hybrid search (fast, basic)
    - "graph": Search + graph expansion (unique value prop)

    Args:
        client: HyperX client instance
        strategy: Retrieval strategy ("search" or "graph")
        k: Number of documents to return
        max_hops: For graph strategy, max hops to expand (default: 2)
        expand_types: For graph strategy, entity types to expand through
        include_paths: For graph strategy, include path descriptions

    Example:
        >>> retriever = HyperXRetriever(client=db, strategy="search", k=10)
        >>> docs = retriever.invoke("React hooks")
    """

    client: Any  # HyperX or AsyncHyperX
    strategy: Literal["search", "graph"] = "search"
    k: int = 10
    max_hops: int = 2
    expand_types: list[str] | None = None
    include_paths: bool = True

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: CallbackManagerForRetrieverRun,
    ) -> list[Document]:
        """Get documents relevant to query.

        Args:
            query: Search query string
            run_manager: Callback manager (unused but required by interface)

        Returns:
            List of Documents from hyperedges
        """
        if self.strategy == "search":
            return self._search_strategy(query)
        elif self.strategy == "graph":
            return self._graph_strategy(query)
        else:
            raise ValueError(f"Unknown strategy: {self.strategy}")

    def _search_strategy(self, query: str) -> list[Document]:
        """Simple search strategy - just wrap db.search()."""
        result = self.client.search(query, limit=self.k)
        return self._hyperedges_to_documents(result.hyperedges, distance=0)

    def _graph_strategy(self, query: str) -> list[Document]:
        """Graph-enhanced strategy - search + path expansion.

        Will be fully implemented in Task 4.
        """
        # For now, fall back to search strategy
        return self._search_strategy(query)

    def _hyperedges_to_documents(
        self,
        hyperedges: list,
        distance: int = 0,
    ) -> list[Document]:
        """Convert hyperedges to LangChain Documents.

        Args:
            hyperedges: List of Hyperedge objects
            distance: Graph distance from original query (0 = direct match)

        Returns:
            List of Documents
        """
        docs = []
        for edge in hyperedges:
            metadata = {
                "id": edge.id,
                "members": [
                    {"entity_id": m.entity_id, "role": m.role}
                    for m in edge.members
                ],
                "distance": distance,
                "source": "hyperx",
            }
            # Add temporal fields if present
            if hasattr(edge, "valid_from") and edge.valid_from:
                metadata["valid_from"] = edge.valid_from.isoformat()
            if hasattr(edge, "valid_until") and edge.valid_until:
                metadata["valid_until"] = edge.valid_until.isoformat()

            docs.append(
                Document(
                    page_content=edge.description,
                    metadata=metadata,
                )
            )
        return docs


class HyperXRetrievalPipeline(BaseRetriever):
    """Full retrieval pipeline with hybrid search and reranking.

    Placeholder - will be implemented in Task 5.
    """

    client: Any

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: CallbackManagerForRetrieverRun,
    ) -> list[Document]:
        raise NotImplementedError(
            "HyperXRetrievalPipeline will be implemented in Task 5"
        )
