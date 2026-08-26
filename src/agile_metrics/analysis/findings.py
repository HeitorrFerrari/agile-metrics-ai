from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class Severity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Finding(BaseModel):
    rule_id: str
    severity: Severity
    title: str
    detail: str
    evidence: dict = Field(default_factory=dict)  # numbers / card ids backing the claim
