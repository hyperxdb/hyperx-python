"""LangChain integration for HyperX.

Install: pip install hyperx[langchain]
"""

from __future__ import annotations

try:
    from langchain_core.retrievers import BaseRetriever
    from langchain_core.documents import Document
    from langchain_core.callbacks import CallbackManagerForRetrieverRun
except ImportError as e:
    raise ImportError(
        "LangChain integration requires langchain-core. "
        "Install with: pip install hyperx[langchain]"
    ) from e

__all__ = ["HyperXRetriever", "HyperXRetrievalPipeline"]


class HyperXRetriever(BaseRetriever):
    """Placeholder - will be implemented in Task 3."""
    pass


class HyperXRetrievalPipeline(BaseRetriever):
    """Placeholder - will be implemented in Task 5."""
    pass
