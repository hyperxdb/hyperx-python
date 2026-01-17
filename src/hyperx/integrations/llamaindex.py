"""LlamaIndex integration for HyperX.

Install: pip install hyperx[llamaindex]
"""

from __future__ import annotations

try:
    from llama_index.core.retrievers import BaseRetriever as LlamaBaseRetriever
    from llama_index.core.schema import NodeWithScore, TextNode
except ImportError as e:
    raise ImportError(
        "LlamaIndex integration requires llama-index-core. "
        "Install with: pip install hyperx[llamaindex]"
    ) from e

__all__ = ["HyperXKnowledgeGraph"]


class HyperXKnowledgeGraph:
    """Placeholder - will be implemented in Task 6."""
    pass
