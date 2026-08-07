"""
Chart aggregation engine.

Responsible for transforming raw data into chart-ready datasets.
"""

from typing import List

import pandas as pd

from .models import (
    Aggregation,
    ChartSpec,
    ChartType,
)


def generate_chart_data(
    df: pd.DataFrame,
    chart: ChartSpec,
) -> List[dict]:

    if chart.chart_type == ChartType.BAR:
        return _bar_chart(df, chart)

    if chart.chart_type == ChartType.LINE:
        return _line_chart(df, chart)

    if chart.chart_type == ChartType.PIE:
        return _pie_chart(df, chart)

    if chart.chart_type == ChartType.SCATTER:
        return _scatter_chart(df, chart)

    if chart.chart_type == ChartType.HISTOGRAM:
        return _histogram(df, chart)

    if chart.chart_type == ChartType.HEATMAP:
        return _heatmap(df)

    if chart.chart_type == ChartType.BOXPLOT:
        return _boxplot(df, chart)

    return []


def _bar_chart(
    df: pd.DataFrame,
    chart: ChartSpec,
) -> List[dict]:

    x = chart.x.column
    y = chart.y.column

    grouped = df.groupby(x)[y]

    if chart.aggregation == Aggregation.SUM:
        result = grouped.sum()

    elif chart.aggregation == Aggregation.MEAN:
        result = grouped.mean()

    elif chart.aggregation == Aggregation.COUNT:
        result = grouped.count()

    elif chart.aggregation == Aggregation.MIN:
        result = grouped.min()

    elif chart.aggregation == Aggregation.MAX:
        result = grouped.max()

    elif chart.aggregation == Aggregation.MEDIAN:
        result = grouped.median()

    else:
        result = grouped.sum()

    return (
        result
        .reset_index()
        .round(4)
        .to_dict("records")
    )

def _line_chart(
    df: pd.DataFrame,
    chart: ChartSpec,
) -> List[dict]:

    x = chart.x.column
    y = chart.y.column

    grouped = (
        df
        .groupby(x)[y]
        .sum()
        .reset_index()
        .sort_values(x)
    )

    return grouped.to_dict("records")

def _pie_chart(
    df: pd.DataFrame,
    chart: ChartSpec,
) -> List[dict]:

    column = chart.x.column

    counts = (
        df[column]
        .value_counts(dropna=False)
        .rename_axis(column)
        .reset_index(name="count")
    )

    return counts.to_dict("records")

def _scatter_chart(
    df: pd.DataFrame,
    chart: ChartSpec,
) -> List[dict]:

    return (
        df[
            [
                chart.x.column,
                chart.y.column,
            ]
        ]
        .dropna()
        .to_dict("records")
    )

def _histogram(
    df: pd.DataFrame,
    chart: ChartSpec,
    bins: int = 20,
) -> List[dict]:

    column = chart.x.column

    frequencies = (
        pd.cut(
            df[column],
            bins=bins,
        )
        .value_counts(sort=False)
    )

    rows = []

    for interval, count in frequencies.items():

        rows.append({
            "binStart": float(interval.left),
            "binEnd": float(interval.right),
            "count": int(count),
        })

    return rows

def _heatmap(
    df: pd.DataFrame,
) -> List[dict]:

    corr = (
        df
        .select_dtypes("number")
        .corr()
    )

    rows = []

    for row in corr.index:
        for column in corr.columns:

            rows.append(
                {
                    "x": row,
                    "y": column,
                    "value": round(
                        float(corr.loc[row, column]),
                        4,
                    ),
                }
            )

    return rows

def _boxplot(
    df: pd.DataFrame,
    chart: ChartSpec,
) -> List[dict]:

    grouped = (
        df.groupby(chart.x.column)[chart.y.column]
    )

    rows = []

    for group, values in grouped:

        values = values.dropna()

        rows.append(
            {
                chart.x.column: group,
                "min": float(values.min()),
                "q1": float(values.quantile(0.25)),
                "median": float(values.median()),
                "q3": float(values.quantile(0.75)),
                "max": float(values.max()),
            }
        )

    return rows