"""
Base Diligence Agent & Material Finding Data Models.
Standardized diligence contract across accounting, infrastructure, IP, and cyber domains.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any


class FindingSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass
class DiligenceFinding:
    """An identified material diligence finding with quantitative valuation impact."""
    id: str
    category: str  # FIN, GPU, IP, CYBER, COMMERCIAL
    title: str
    severity: FindingSeverity
    ebitda_haircut_usd: float = 0.0
    multiple_discount: float = 0.0
    direct_liability_usd: float = 0.0
    escrow_hold_usd: float = 0.0
    description: str = ""
    source_docs: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "category": self.category,
            "title": self.title,
            "severity": self.severity.value,
            "ebitda_haircut_usd": round(self.ebitda_haircut_usd, 2),
            "multiple_discount": round(self.multiple_discount, 2),
            "direct_liability_usd": round(self.direct_liability_usd, 2),
            "escrow_hold_usd": round(self.escrow_hold_usd, 2),
            "description": self.description,
            "source_docs": self.source_docs,
        }


class BaseDiligenceAgent(ABC):
    """Abstract interface for specialist diligence agents."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def audit(self) -> List[DiligenceFinding]:
        """Execute domain-specific diligence and return quantified material findings."""
        pass
