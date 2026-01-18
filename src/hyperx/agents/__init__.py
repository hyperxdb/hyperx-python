"""HyperX agent tools for agentic RAG workflows.

This module provides base classes, protocols, and ready-to-use tools
for building agent systems that integrate with LLM frameworks.

Example:
    >>> from hyperx import HyperX
    >>> from hyperx.agents import SearchTool, PathsTool, QualitySignals, ToolResult
    >>>
    >>> # Use ready-to-use SearchTool
    >>> client = HyperX(api_key="hx_sk_...")
    >>> search = SearchTool(client, mode="hybrid", default_limit=10)
    >>> result = search.run(query="react hooks")
    >>> if result.quality.should_retrieve_more:
    ...     print("Consider retrieving more data")
    >>>
    >>> # Use PathsTool for multi-hop reasoning
    >>> paths_tool = PathsTool(client, default_max_hops=4)
    >>> result = paths_tool.run(from_entity="e:useState", to_entity="e:redux")
    >>> if result.success:
    ...     for path in result.data["paths"]:
    ...         print(f"Path via: {path['hyperedges']}")
    >>>
    >>> # Or implement your own tool
    >>> class MySearchTool:
    ...     @property
    ...     def name(self) -> str:
    ...         return "my_search"
    ...
    ...     @property
    ...     def description(self) -> str:
    ...         return "Search the knowledge graph"
    ...
    ...     def run(self, query: str) -> ToolResult:
    ...         # Implementation here
    ...         pass
    ...
    ...     async def arun(self, query: str) -> ToolResult:
    ...         # Async implementation here
    ...         pass
    ...
    ...     def to_openai_schema(self) -> dict:
    ...         return {
    ...             "type": "function",
    ...             "function": {
    ...                 "name": self.name,
    ...                 "description": self.description,
    ...                 "parameters": {
    ...                     "type": "object",
    ...                     "properties": {
    ...                         "query": {"type": "string"}
    ...                     },
    ...                     "required": ["query"]
    ...                 }
    ...             }
    ...         }
"""

from hyperx.agents.base import (
    BaseTool,
    QualitySignals,
    ToolError,
    ToolResult,
)
from hyperx.agents.quality import QualityAnalyzer
from hyperx.agents.tools import PathsTool, SearchTool

__all__ = [
    "BaseTool",
    "PathsTool",
    "QualityAnalyzer",
    "QualitySignals",
    "SearchTool",
    "ToolError",
    "ToolResult",
]
