"""
Trend statistics engine.

Computes statistical evidence required for a TrendPlan.
"""

import pandas as pd


def generate_trend_statistics(
    df: pd.DataFrame,
    plan,
) -> dict:

    if plan.analysis_type == "time_series":
        return _time_series(
            df,
            plan,
        )

    if plan.analysis_type == "growth_rate":
        return _growth_rate(
            df,
            plan,
        )

    if plan.analysis_type == "moving_average":
        return _moving_average(
            df,
            plan,
        )

    raise ValueError(
        f"Unsupported trend analysis "
        f"'{plan.analysis_type}'."
    )

def _bucket_time(
    series: pd.Series,
    frequency: str,
) -> pd.Series:

    if frequency == "hour":
        return series.dt.floor("h")

    if frequency == "day":
        return series.dt.floor("D")

    if frequency == "week":
        return series.dt.to_period("W").dt.start_time

    if frequency == "month":
        return series.dt.to_period("M").dt.start_time

    raise ValueError(
        f"Unsupported trend frequency "
        f"'{frequency}'."
    )

def _time_series(
    df: pd.DataFrame,
    plan,
) -> dict:

    time = plan.time_column
    metric = plan.metric
    aggregation = plan.aggregation
    frequency = plan.frequency

    data = (
        df[
            [
                time,
                metric,
            ]
        ]
        .dropna(subset=[time])
        .copy()
    )

    # --------------------------------------------------
    # Ensure datetime
    # --------------------------------------------------

    data[time] = pd.to_datetime(
        data[time],
        errors="coerce",
    )

    data = data.dropna(
        subset=[time]
    )

    # --------------------------------------------------
    # Apply time frequency
    # --------------------------------------------------

    if frequency == "hour":

        data["__period"] = (
            data[time]
            .dt.floor("h")
        )

    elif frequency == "day":

        data["__period"] = (
            data[time]
            .dt.floor("D")
        )

    elif frequency == "week":

        data["__period"] = (
            data[time]
            .dt.to_period("W")
            .dt.start_time
        )

    elif frequency == "month":

        data["__period"] = (
            data[time]
            .dt.to_period("M")
            .dt.start_time
        )

    else:
        raise ValueError(
            f"Unsupported frequency '{frequency}'."
        )

    # --------------------------------------------------
    # Aggregate
    # --------------------------------------------------

    grouped = data.groupby(
        "__period"
    )

    if aggregation == "count":

        result = (
            grouped[metric]
            .count()
            .reset_index(
                name="value"
            )
        )

    elif aggregation == "mean":

        result = (
            grouped[metric]
            .mean()
            .reset_index(
                name="value"
            )
        )

    elif aggregation == "sum":

        result = (
            grouped[metric]
            .sum()
            .reset_index(
                name="value"
            )
        )

    elif aggregation == "min":

        result = (
            grouped[metric]
            .min()
            .reset_index(
                name="value"
            )
        )

    elif aggregation == "max":

        result = (
            grouped[metric]
            .max()
            .reset_index(
                name="value"
            )
        )

    elif aggregation == "median":

        result = (
            grouped[metric]
            .median()
            .reset_index(
                name="value"
            )
        )

    else:
        raise ValueError(
            f"Unsupported aggregation "
            f"'{aggregation}'."
        )

    result = result.sort_values(
        "__period"
    )

    result = result.round(4)

    # --------------------------------------------------
    # Rename period back to time column
    # --------------------------------------------------

    result = result.rename(
        columns={
            "__period": time
        }
    )

    rows = result.to_dict(
        "records"
    )

    if not rows:

        return {
            "trend_type": "time_series",

            "time_column": time,
            "metric": metric,

            "aggregation": aggregation,
            "frequency": frequency,

            "points": [],

            "sample_size": 0,
        }

    # --------------------------------------------------
    # First / Last
    # --------------------------------------------------

    first = rows[0]["value"]
    last = rows[-1]["value"]

    change = last - first

    if first != 0:

        percentage_change = (
            change /
            abs(first)
        ) * 100

    else:

        percentage_change = None

    return {

        "trend_type": "time_series",

        "time_column": time,

        "metric": metric,

        "aggregation": aggregation,

        "frequency": frequency,

        "points": rows,

        "first_value": first,

        "last_value": last,

        "change": round(
            float(change),
            4,
        ),

        "percentage_change": (
            round(
                float(
                    percentage_change
                ),
                4,
            )
            if percentage_change is not None
            else None
        ),

        "sample_size": len(data),
    }

def _growth_rate(
    df: pd.DataFrame,
    plan,
) -> dict:

    time = plan.time_column
    metric = plan.metric

    data = (
        df[
            [
                time,
                metric,
            ]
        ]
        .dropna()
        .sort_values(time)
    )

    grouped = (
        data
        .groupby(time)[metric]
        .mean()
        .reset_index()
        .sort_values(time)
    )

    grouped["growth_rate"] = (
        grouped[metric]
        .pct_change()
        .mul(100)
    )

    grouped = grouped.round(4)

    return {
        "trend_type": "growth_rate",

        "time_column": time,
        "metric": metric,

        "points": grouped.to_dict(
            "records"
        ),

        "sample_size": len(data),
    }


# --------------------------------------------------
# Moving Average
# --------------------------------------------------

def _moving_average(
    df: pd.DataFrame,
    plan,
) -> dict:

    time = plan.time_column
    metric = plan.metric

    window = getattr(
        plan,
        "window",
        3,
    )

    data = (
        df[
            [
                time,
                metric,
            ]
        ]
        .dropna()
        .sort_values(time)
    )

    grouped = (
        data
        .groupby(time)[metric]
        .mean()
        .reset_index()
        .sort_values(time)
    )

    grouped["moving_average"] = (
        grouped[metric]
        .rolling(window)
        .mean()
    )

    grouped = grouped.round(4)

    return {
        "trend_type": "moving_average",

        "time_column": time,
        "metric": metric,

        "window": window,

        "points": grouped.to_dict(
            "records"
        ),

        "sample_size": len(data),
    }