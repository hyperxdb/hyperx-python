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
    from langchain_core.callbacks import (
        AsyncCallbackManagerForRetrieverRun,
        CallbackManagerForRetrieverRun,
    )
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

    async def _aget_relevant_documents(
        self,
        query: str,
        *,
        run_manager: AsyncCallbackManagerForRetrieverRun,
    ) -> list[Document]:
        """Async version - delegates to sync for now."""
        return self._get_relevant_documents(query, run_manager=run_manager)  # type: ignore

    def _search_strategy(self, query: str) -> list[Document]:
        """Simple search strategy - just wrap db.search()."""
        result = self.client.search(query, limit=self.k)
        return self._hyperedges_to_documents(result.hyperedges, distance=0)

    def _graph_strategy(self, query: str) -> list[Document]:
        """Graph-enhanced strategy - search + path expansion.

        1. Run initial search
        2. For each entity in results, find paths to related entities
        3. Collect hyperedges from paths
        4. Deduplicate and return
        """
        # Step 1: Initial search
        result = self.client.search(query, limit=self.k)
        docs = self._hyperedges_to_documents(result.hyperedges, distance=0)
        seen_ids = {edge.id for edge in result.hyperedges}

        # Step 2: Get entity IDs to expand (filter by type if specified)
        entity_ids = [e.id for e in result.entities]
        if self.expand_types:
            entity_ids = [
                e.id for e in result.entities if e.entity_type in self.expand_types
            ]

        # Step 3: Find paths from each entity pair (limit to top 5 entities)
        expanded_edges = []
        entities_to_expand = entity_ids[:5]

        for i, source_id in enumerate(entities_to_expand):
            # Try to find paths to other entities in results
            for target_id in entities_to_expand[i + 1 :]:
                try:
                    paths = self.client.paths.find(
                        from_entity=source_id,
                        to_entity=target_id,
                        max_hops=self.max_hops,
                        k_paths=self.k,
                    )
                    for path in paths:
                        hops = len(path.hyperedges)
                        for edge_id in path.hyperedges:
                            if edge_id not in seen_ids:
                                seen_ids.add(edge_id)
                                # Fetch full hyperedge object
                                try:
                                    edge = self.client.hyperedges.get(edge_id)
                                    expanded_edges.append((edge, hops))
                                except Exception:
                                    # Skip if hyperedge fetch fails
                                    continue
                except Exception:
                    # Skip if path finding fails for this entity pair
                    continue

        # Step 4: Add expanded edges with distance metadata
        for edge, hops in expanded_edges:
            docs.extend(self._hyperedges_to_documents([edge], distance=hops))

        # Return up to k documents
        return docs[: self.k]

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
