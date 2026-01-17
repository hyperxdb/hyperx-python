"""Tests for LangChain integration."""

from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest
from pydantic import ValidationError

from hyperx import Entity, Hyperedge, HyperedgeMember, SearchResult
from hyperx.integrations.langchain import HyperXRetriever


@pytest.fixture
def mock_client():
    """Create a mock HyperX client."""
    client = MagicMock()
    now = datetime.now(timezone.utc)
    client.search.return_value = SearchResult(
        entities=[
            Entity(
                id="e:react",
                name="React",
                entity_type="technology",
                attributes={},
                created_at=now,
                updated_at=now,
            )
        ],
        hyperedges=[
            Hyperedge(
                id="h:1",
                description="React provides Hooks for state management",
                members=[
                    HyperedgeMember(entity_id="e:react", role="subject"),
                    HyperedgeMember(entity_id="e:hooks", role="object"),
                ],
                attributes={},
                created_at=now,
                updated_at=now,
            )
        ],
    )
    return client


def test_retriever_search_strategy(mock_client):
    """Test retriever with simple search strategy."""
    retriever = HyperXRetriever(client=mock_client, strategy="search", k=5)

    docs = retriever.invoke("React state management")

    assert len(docs) == 1
    assert "React provides Hooks" in docs[0].page_content
    assert docs[0].metadata["id"] == "h:1"
    mock_client.search.assert_called_once_with("React state management", limit=5)


def test_retriever_default_strategy(mock_client):
    """Test retriever defaults to search strategy."""
    retriever = HyperXRetriever(client=mock_client, k=10)

    docs = retriever.invoke("test query")

    assert len(docs) == 1
    mock_client.search.assert_called_once()


def test_retriever_document_metadata(mock_client):
    """Test that document metadata is properly populated."""
    retriever = HyperXRetriever(client=mock_client, strategy="search", k=5)

    docs = retriever.invoke("test")

    assert docs[0].metadata["id"] == "h:1"
    assert docs[0].metadata["source"] == "hyperx"
    assert docs[0].metadata["distance"] == 0
    assert "members" in docs[0].metadata


def test_retriever_invalid_strategy(mock_client):
    """Test that invalid strategy raises ValidationError at construction."""
    with pytest.raises(ValidationError, match="Input should be 'search' or 'graph'"):
        HyperXRetriever(client=mock_client, strategy="invalid", k=5)


def test_retriever_graph_strategy_not_implemented(mock_client):
    """Test that graph strategy raises NotImplementedError."""
    retriever = HyperXRetriever(client=mock_client, strategy="graph", k=5)

    with pytest.raises(NotImplementedError, match="Graph strategy"):
        retriever.invoke("test")


def test_retriever_empty_results():
    """Test retriever handles empty search results."""
    client = MagicMock()
    client.search.return_value = SearchResult(entities=[], hyperedges=[])

    retriever = HyperXRetriever(client=client, strategy="search", k=5)
    docs = retriever.invoke("nonexistent")

    assert docs == []
