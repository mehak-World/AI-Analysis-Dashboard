"""
Candidate scoring.

Assigns each ChartSpec candidate a 0-100 business-relevance score
based on: keyword weight (does this look like a metric a business
actually cares about?), statistical strength (correlation), and
cardinality fit. This is what replaces "first structurally valid
chart wins" with charts actually ranked by usefulness.

Tune _HIGH_VALUE_KEYWORDS and _TYPE_BASE_SCORE per your domain —
these are deliberately just data, not logic, so you can adjust them
without touching the scoring flow.
"""
from typing import List

from .models import ChartSpec, ChartType

_HIGH_VALUE_KEYWORDS = [
    "revenue", "sales", "profit", "cost", "price", "margin",
    "conversion", "churn", "retention", "growth", "roi", "spend",
    "satisfaction", "rating", "score", "salary", "budget",
]

_TYPE_BASE_SCORE = {
    ChartType.LINE: 65,
    ChartType.BAR: 60,
    ChartType.HEATMAP: 50,
    ChartType.SCATTER: 55,
    ChartType.PIE: 40,
    ChartType.HISTOGRAM: 35,
    ChartType.BOXPLOT: 30,
}


def score_candidates(candidates: List[ChartSpec]) -> List[ChartSpec]:
    for chart in candidates:
        chart.priority = _score_one(chart)
    return candidates


def _score_one(chart: ChartSpec) -> int:
    score = _TYPE_BASE_SCORE.get(chart.chart_type, 30)

    score += _keyword_bonus(chart.x.column if chart.x else "")
    score += _keyword_bonus(chart.y.column if chart.y else "")

    if chart.chart_type in (ChartType.BAR, ChartType.PIE):
        cardinality = chart.options.get("dimension_cardinality")
        if cardinality:
            # Sweet spot for a readable bar/pie: 3-8 categories.
            if 3 <= cardinality <= 8:
                score += 15
            elif cardinality > 15:
                score -= 15

    if chart.chart_type == ChartType.SCATTER:
        correlation = abs(chart.options.get("correlation", 0))
        score += int(correlation * 30)

    if chart.chart_type == ChartType.LINE:
        score += 10  # trends over time are almost always worth showing

    return max(0, min(100, score))


def _keyword_bonus(column_name: str) -> int:
    name = (column_name or "").lower()
    return 15 if any(kw in name for kw in _HIGH_VALUE_KEYWORDS) else 0