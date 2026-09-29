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

    # --------------------------------------------------
    # Rate by Category
    # --------------------------------------------------

    if chart.options.get("metric") == "rate":

        positive_value = chart.options.get(
            "positive_value"
        )

        if positive_value is None:
            raise ValueError(
                "Rate chart requires a positive_value."
            )

        data = (
            df[
                [
                    x,
                    y,
                ]
            ]
            .dropna()
        )

        grouped = data.groupby(x)

        total = grouped[y].size()

        positive_count = (
            (data[y] == positive_value)
            .groupby(data[x])
            .sum()
        )

        result = (
            positive_count
            .div(total)
            .mul(100)
            .rename(y)
        )

        return (
            result
            .reset_index()
            .round(2)
            .to_dict("records")
        )

    # --------------------------------------------------
    # Normal Bar Aggregations
    # --------------------------------------------------

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

    data = df[[x, y]].copy()

    # --------------------------------------------------
    # Parse datetime
    # --------------------------------------------------

    data[x] = pd.to_datetime(
        data[x],
        errors="coerce",
    )

    data = data.dropna(
        subset=[x]
    )

    # --------------------------------------------------
    # Frequency
    # --------------------------------------------------

    frequency = chart.options.get(
        "frequency",
        "day",
    )

    if frequency == "hour":
        data["_period"] = data[x].dt.floor("h")

    elif frequency == "day":
        data["_period"] = data[x].dt.floor("D")

    elif frequency == "week":
        data["_period"] = (
            data[x]
            .dt.to_period("W")
            .dt.start_time
        )

    elif frequency == "month":
        data["_period"] = (
            data[x]
            .dt.to_period("M")
            .dt.start_time
        )

    elif frequency == "quarter":
        data["_period"] = (
            data[x]
            .dt.to_period("Q")
            .dt.start_time
        )

    elif frequency == "year":
        data["_period"] = (
            data[x]
            .dt.to_period("Y")
            .dt.start_time
        )

    else:
        raise ValueError(
            f"Unsupported trend frequency: {frequency}"
        )

    # --------------------------------------------------
    # Aggregation
    # --------------------------------------------------

    aggregation = chart.aggregation

    if aggregation == Aggregation.COUNT:

        grouped = (
            data
            .groupby("_period")
            .size()
            .reset_index(name=y)
        )

    elif aggregation == Aggregation.SUM:

        grouped = (
            data
            .groupby("_period")[y]
            .sum()
            .reset_index()
        )

    elif aggregation == Aggregation.MEAN:

        grouped = (
            data
            .groupby("_period")[y]
            .mean()
            .reset_index()
        )

    elif aggregation == Aggregation.MIN:

        grouped = (
            data
            .groupby("_period")[y]
            .min()
            .reset_index()
        )

    elif aggregation == Aggregation.MAX:

        grouped = (
            data
            .groupby("_period")[y]
            .max()
            .reset_index()
        )

    elif aggregation == Aggregation.MEDIAN:

        grouped = (
            data
            .groupby("_period")[y]
            .median()
            .reset_index()
        )

    else:

        grouped = (
            data
            .groupby("_period")[y]
            .sum()
            .reset_index()
        )

    # --------------------------------------------------
    # Final format
    # --------------------------------------------------

    grouped = grouped.rename(
        columns={
            "_period": x,
        }
    )

    return (
        grouped
        .sort_values(x)
        .round(4)
        .to_dict("records")
    )

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