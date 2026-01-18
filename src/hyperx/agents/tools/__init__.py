"""HyperX agent tools for agentic RAG workflows.

This module provides ready-to-use tools for building agentic RAG
systems with LLM frameworks like OpenAI, LangChain, and others.

Example:
    >>> from hyperx import HyperX
    >>> from hyperx.agents.tools import SearchTool, PathsTool
    >>>
    >>> client = HyperX(api_key="hx_sk_...")
    >>> search = SearchTool(client, mode="hybrid", default_limit=10)
    >>>
    >>> # Use with OpenAI function calling
    >>> schema = search.to_openai_schema()
    >>>
    >>> # Execute search
    >>> result = search.run(query="react state management")
    >>> if result.quality.should_retrieve_more:
    ...     # Agent decides to retrieve more
    ...     result = search.run(query=result.quality.alternative_queries[0])
    >>>
    >>> # Find multi-hop paths between entities
    >>> paths_tool = PathsTool(client, default_max_hops=4)
    >>> result = paths_tool.run(from_entity="e:useState", to_entity="e:redux")
    >>> if result.success:
    ...     for path in result.data["paths"]:
    ...         print(f"Path cost: {path['cost']}")
"""

from hyperx.agents.tools.paths import PathsTool
from hyperx.agents.tools.search import SearchTool

__all__ = [
    "PathsTool",
    "SearchTool",
]
