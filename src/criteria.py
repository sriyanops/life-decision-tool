# src/criteria.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Criterion:
    key: str
    label: str
    help: str
    min_value: int = 0
    max_value: int = 10
    default: int = 5
    weight: float = 1.0


# Category-specific criteria (v0)
CRITERIA_BY_CATEGORY: Dict[str, List[Criterion]] = {
    "Career": [
        Criterion("skill_compounding", "Skill compounding", "Does this build transferable skills that stack over time?", weight=1.3),
        Criterion("resume_signal", "Resume signal", "How strongly does this signal competence to employers?", weight=1.2),
        Criterion("upside", "Upside", "Ceiling over 2–5 years if executed well.", weight=1.1),
        Criterion("optionality", "Optionality", "Does this keep doors open / reduce lock-in?", weight=1.0),
        Criterion("day_to_day_fit", "Day-to-day fit", "Do you realistically like the daily work?", weight=0.9),
    ],
    "Financial": [
        Criterion("expected_roi", "Expected ROI", "Expected financial return relative to effort/time.", weight=1.3),
        Criterion("cashflow_timing", "Cashflow timing", "How quickly benefits arrive.", weight=1.1),
        Criterion("volatility", "Stability", "How predictable the outcome is (higher = more stable).", weight=1.2),
        Criterion("simplicity", "Simplicity", "How easy it is to execute and maintain.", weight=0.9),
    ],
    "Relationship": [
        Criterion("trust", "Trust impact", "Does this increase trust and stability?", weight=1.3),
        Criterion("conflict_risk", "Conflict reduction", "Does this reduce recurring conflict?", weight=1.1),
        Criterion("long_term_alignment", "Long-term alignment", "Are values + trajectory aligned?", weight=1.2),
        Criterion("repairability", "Repairability", "If it goes wrong, can it be repaired?", weight=1.0),
    ],
    "Health": [
        Criterion("health_outcome", "Health outcome", "Expected improvement to health/fitness.", weight=1.3),
        Criterion("adherence", "Adherence", "How likely you are to stick with it.", weight=1.2),
        Criterion("energy", "Energy / mood", "Impact on energy and mood.", weight=1.0),
        Criterion("sustainability", "Sustainability", "Can you maintain it long-term?", weight=1.1),
    ],
    "Personal": [
        Criterion("quality_of_life", "Quality of life", "Does it improve your life overall?", weight=1.2),
        Criterion("identity_fit", "Identity fit", "Does this fit who you want to be?", weight=1.1),
        Criterion("regret_minimization", "Regret minimization", "Will you regret not doing this?", weight=1.0),
        Criterion("simplicity", "Simplicity", "Execution simplicity / low friction.", weight=0.9),
    ],
}


def criteria_for(category: str) -> List[Criterion]:
    return CRITERIA_BY_CATEGORY.get(category, CRITERIA_BY_CATEGORY["Personal"])


def weighted_score(category: str, values: Dict[str, int]) -> float:
    crits = criteria_for(category)
    total_w = sum(c.weight for c in crits)
    if total_w <= 0:
        return 0.0

    s = 0.0
    for c in crits:
        v = int(values.get(c.key, c.default))
        v = max(c.min_value, min(c.max_value, v))
        s += v * c.weight

    # Normalize to 0–100
    max_raw = sum(c.max_value * c.weight for c in crits)
    if max_raw <= 0:
        return 0.0
    return (s / max_raw) * 100.0
