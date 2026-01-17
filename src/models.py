# src/models.py
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List


class Risk(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


@dataclass
class Limits:
    # Locked user-facing limits (STRICT-4)
    money_max_usd: int = 1000
    time_hours_per_week: int = 10
    stress: Risk = Risk.MEDIUM
    relationships: Risk = Risk.MEDIUM

    # Legacy / future limits (kept for safety, NOT enforced in v0.1)
    reversibility: Risk = Risk.MEDIUM
    dependency: Risk = Risk.MEDIUM

    confirmed: bool = False


@dataclass
class Decision:
    title: str = ""
    category: str = ""
    limits: Limits = field(default_factory=Limits)


@dataclass
class OptionInput:
    name: str

    # HARD guardrail inputs (compared against Limits) (STRICT-4)
    money_at_risk_usd: int = 1000
    time_required_hours_per_week: int = 10
    stress_fit: Risk = Risk.MEDIUM
    relationships_impact: Risk = Risk.MEDIUM

    # Legacy / future (kept, not yet surfaced or enforced)
    reversibility: Risk = Risk.MEDIUM
    dependency: Risk = Risk.MEDIUM

    # Non-scored grounding text
    summary: str = ""

    # Category-specific structured criteria (0–10 sliders)
    criteria: Dict[str, int] = field(default_factory=dict)


def check_limits(limits: Limits, opt: OptionInput) -> Dict[str, bool]:
    """
    Hard pass/fail comparison.

    v0.1 STRICT-4:
      - Money (numeric)
      - Time (hours/week)
      - Stress (Low/Med/High)
      - Relationships (Low/Med/High)

    Legacy fields (reversibility/dependency) are intentionally NOT enforced yet.
    """
    order = {Risk.LOW: 0, Risk.MEDIUM: 1, Risk.HIGH: 2}

    def ok(tolerance: Risk, actual: Risk) -> bool:
        return order[actual] <= order[tolerance]

    return {
        # IMPORTANT: key is "financial" to match Compare UX + CHECK_ORDER
        "financial": int(opt.money_at_risk_usd) <= int(limits.money_max_usd),
        "time": int(opt.time_required_hours_per_week) <= int(limits.time_hours_per_week),
        "stress": ok(limits.stress, opt.stress_fit),
        "relationships": ok(limits.relationships, opt.relationships_impact),
    }


DEFAULT_CATEGORIES: List[str] = [
    "Career",
    "Personal",
    "Financial",
    "Relationship",
    "Health",
]

