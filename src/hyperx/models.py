"""Data models for HyperX SDK."""

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class Entity(BaseModel):
    """A node in the hypergraph."""

    id: str
    name: str
    entity_type: str
    attributes: dict[str, Any] = Field(default_factory=dict)
    confidence: float = 1.0
    created_at: datetime
    updated_at: datetime
    # Temporal fields
    valid_from: datetime | None = None
    valid_until: datetime | None = None
    state: Literal["active", "deprecated", "superseded", "retired"] = "active"
    version: int = 1
    predecessor_id: str | None = None
    chain_root_id: str | None = None


class HyperedgeMember(BaseModel):
    """A member of a hyperedge."""

    entity_id: str
    role: str


class Hyperedge(BaseModel):
    """An n-ary relationship connecting multiple entities."""

    id: str
    description: str
    members: list[HyperedgeMember]
    attributes: dict[str, Any] = Field(default_factory=dict)
    confidence: float = 1.0
    created_at: datetime
    updated_at: datetime
    # Temporal fields
    valid_from: datetime | None = None
    valid_until: datetime | None = None
    state: Literal["active", "deprecated", "superseded", "retired"] = "active"
    version: int = 1
    predecessor_id: str | None = None
    chain_root_id: str | None = None


class SearchResult(BaseModel):
    """Results from a search query."""

    entities: list[Entity]
    hyperedges: list[Hyperedge]


class PathResult(BaseModel):
    """A path between two entities."""

    hyperedges: list[str]
    bridges: list[list[str]]
    cost: float


class PathsResponse(BaseModel):
    """Response from paths.find()."""

    paths: list[PathResult]


class Webhook(BaseModel):
    """A webhook subscription."""

    id: str
    url: str
    events: list[str]
    secret: str | None = None
    active: bool = True
    created_at: datetime
    updated_at: datetime


class WebhookDelivery(BaseModel):
    """Record of a webhook delivery attempt."""

    id: str
    webhook_id: str
    event_type: str
    payload: dict[str, Any]
    status_code: int | None = None
    response_body: str | None = None
    delivered_at: datetime | None = None
    attempts: int = 0
    success: bool = False
