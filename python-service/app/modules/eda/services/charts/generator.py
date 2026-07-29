"""
Chart generation orchestrator.
"""
from typing import List

import pandas as pd

from .aggregations import generate_chart_data
from .models import ChartSpec
from .statistics import generate_statistics

import re


def generate_chart_id(chart: ChartSpec) -> str:
    parts = [chart.chart_type.value]

    if chart.x:
        parts.append(chart.x.column)

    if chart.y:
        parts.append(chart.y.column)

    return re.sub(r"[^a-zA-Z0-9_]+", "_", "_".join(parts)).lower()

def generate_charts(
    df: pd.DataFrame,
    chart_specs: List[ChartSpec],
) -> List[dict]:
    """
    Generates complete chart objects.
    Input:
        DataFrame
        List[ChartSpec]

    Output:
        List[Chart DTO]
    """

    charts = []

    for chart in chart_specs:
        try:
            chart_data = generate_chart_data(
                df,
                chart,
            )
            if not chart_data:
                continue
            statistics = generate_statistics(
                df,
                chart,
                chart_data,
            )

            charts.append(
                _build_chart(
                    chart,
                    chart_data,
                    statistics,
                )
            )

        except Exception as ex:
            print(
                f"Failed generating chart "
                f"{chart.name}: {ex}"
            )

    return charts

def _build_chart(
    chart: ChartSpec,
    chart_data: list[dict],
    statistics: dict,
) -> dict:

    return {
        "id": generate_chart_id(chart),
        "name": chart.name,
        "type": chart.chart_type.value,
        "reason": chart.reason,
        "config": {
            # Some chart types (e.g. heatmap) have no single x/y column —
            # both chart.x and chart.y can be None, so both need the
            # same guard. Previously only yKey had it, which is what
            # crashed on heatmap.
            "xKey": chart.x.column if chart.x else None,
            "yKey": chart.y.column if chart.y else None,
            "aggregation": chart.aggregation.value,
            "sort": chart.sort.value,
            "options": chart.options,
        },

        "data": chart_data,
        "xAxis": {
            "label": chart.x.label if chart.x else "",
            "unit": chart.x.unit if chart.x else "",
        },

        "yAxis": {
            "label": chart.y.label if chart.y else "",
            "unit": chart.y.unit if chart.y else "",
        },

        "statistics": statistics,

        # Gemini later
        "summary": "",

        # Gemini later
        "insight": "",
    }