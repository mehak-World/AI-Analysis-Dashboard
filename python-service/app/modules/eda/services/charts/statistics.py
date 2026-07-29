"""
Chart statistics engine.

Computes statistics that accompany generated charts.
"""

from typing import Any

import pandas as pd

from .models import ChartSpec, ChartType


def generate_statistics(
    df: pd.DataFrame,
    chart: ChartSpec,
    chart_data: list[dict],
) -> dict[str, Any]:

    if chart.chart_type == ChartType.BAR:
        return _bar_statistics(chart_data)

    if chart.chart_type == ChartType.LINE:
        return _line_statistics(chart_data)

    if chart.chart_type == ChartType.PIE:
        return _pie_statistics(chart_data)

    if chart.chart_type == ChartType.SCATTER:
        return _scatter_statistics(df, chart)

    if chart.chart_type == ChartType.HISTOGRAM:
        return _histogram_statistics(df, chart)

    if chart.chart_type == ChartType.BOXPLOT:
        return _boxplot_statistics(df, chart)

    if chart.chart_type == ChartType.HEATMAP:
        return _heatmap_statistics(df)

    return {}

def _bar_statistics(
    chart_data: list[dict],
) -> dict:

    if not chart_data:
        return {}

    value_key = list(chart_data[0].keys())[1]

    values = [
        row[value_key]
        for row in chart_data
    ]

    return {
        "count": len(values),
        "min": round(min(values), 4),
        "max": round(max(values), 4),
        "mean": round(sum(values) / len(values), 4),
        "total": round(sum(values), 4),
    }

def _line_statistics(
    chart_data: list[dict],
) -> dict:

    if not chart_data:
        return {}

    value_key = list(chart_data[0].keys())[1]

    values = [
        row[value_key]
        for row in chart_data
    ]

    return {
        "points": len(values),
        "min": round(min(values), 4),
        "max": round(max(values), 4),
        "start": values[0],
        "end": values[-1],
        "change": round(values[-1] - values[0], 4),
    }

def _pie_statistics(
    chart_data: list[dict],
) -> dict:

    if not chart_data:
        return {}

    counts = [
        row["count"]
        for row in chart_data
    ]

    total = sum(counts)

    largest = max(chart_data, key=lambda x: x["count"])

    return {
        "categories": len(chart_data),
        "total": total,
        "largestCategory": largest,
    }

def _scatter_statistics(
    df: pd.DataFrame,
    chart: ChartSpec,
) -> dict:

    correlation = (
        df[
            [
                chart.x.column,
                chart.y.column,
            ]
        ]
        .corr()
        .iloc[0, 1]
    )

    return {
        "correlation": round(float(correlation), 4)
    }

def _boxplot_statistics(
    df: pd.DataFrame,
    chart: ChartSpec,
) -> dict:

    series = df[chart.x.column].dropna()

    q1 = series.quantile(.25)
    q3 = series.quantile(.75)

    iqr = q3 - q1

    outliers = series[
        (series < q1 - 1.5 * iqr)
        |
        (series > q3 + 1.5 * iqr)
    ]

    return {
        "min": round(float(series.min()), 4),
        "q1": round(float(q1), 4),
        "median": round(float(series.median()), 4),
        "q3": round(float(q3), 4),
        "max": round(float(series.max()), 4),
        "iqr": round(float(iqr), 4),
        "outlierCount": len(outliers),
    }

def _heatmap_statistics(
    df: pd.DataFrame,
) -> dict:

    corr = (
        df
        .select_dtypes("number")
        .corr()
    )

    max_corr = 0
    strongest = None

    columns = corr.columns

    for i in range(len(columns)):
        for j in range(i + 1, len(columns)):

            value = corr.iloc[i, j]

            if abs(value) > abs(max_corr):
                max_corr = value

                strongest = {
                    "columnA": columns[i],
                    "columnB": columns[j],
                    "correlation": round(float(value), 4),
                }

    return {
        "strongestCorrelation": strongest
    }

def _histogram_statistics(
    df: pd.DataFrame,
    chart: ChartSpec,
) -> dict:

    series = df[chart.x.column].dropna()

    return {
        "count": int(series.count()),
        "mean": round(float(series.mean()), 4),
        "median": round(float(series.median()), 4),
        "std": round(float(series.std()), 4),
        "variance": round(float(series.var()), 4),
        "min": round(float(series.min()), 4),
        "max": round(float(series.max()), 4),
    }