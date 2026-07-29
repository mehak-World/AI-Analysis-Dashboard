"""
Final chart selection.

Takes scored candidates and picks a diverse top-N: highest scoring
charts first, but capped per chart type and de-duplicated on the
same x/y pair — so the dashboard doesn't end up as 8 bar charts and
nothing else.
"""
from collections import defaultdict
from typing import List

from .models import ChartSpec, ChartType

DEFAULT_MAX_CHARTS = 10
MAX_PER_TYPE = {
    ChartType.BAR: 4,
    ChartType.LINE: 3,
    ChartType.SCATTER: 3,
    ChartType.PIE: 2,
    ChartType.HISTOGRAM: 2,
    ChartType.BOXPLOT: 2,
    ChartType.HEATMAP: 1,
}


def select_charts(
    candidates: List[ChartSpec],
    max_charts: int = DEFAULT_MAX_CHARTS,
) -> List[ChartSpec]:

    ranked = sorted(candidates, key=lambda c: c.priority, reverse=True)

    selected: List[ChartSpec] = []
    type_counts = defaultdict(int)
    seen_pairs = set()

    for chart in ranked:
        if len(selected) >= max_charts:
            break

        pair_key = (
            chart.chart_type,
            chart.x.column if chart.x else None,
            chart.y.column if chart.y else None,
        )
        if pair_key in seen_pairs:
            continue

        cap = MAX_PER_TYPE.get(chart.chart_type, 3)
        if type_counts[chart.chart_type] >= cap:
            continue

        selected.append(chart)
        seen_pairs.add(pair_key)
        type_counts[chart.chart_type] += 1

    return selected