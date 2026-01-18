"""HyperX agent tools for agentic RAG workflows.

This module provides base classes and protocols for building
agent tools that integrate with LLM frameworks.

Example:
    >>> from hyperx.agents import BaseTool, QualitySignals, ToolResult
    >>>
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

__all__ = [
    "BaseTool",
    "QualityAnalyzer",
    "QualitySignals",
    "ToolError",
    "ToolResult",
]
