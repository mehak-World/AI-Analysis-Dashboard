"""
Trend analysis planner.

Determines the appropriate trend analysis based
on the selected time and metric columns.

No AI is used here.
"""

from pandas.api.types import (
    is_datetime64_any_dtype,
    is_numeric_dtype,
)

from .models import TrendPlan


IDENTIFIER_COLUMNS = {
    "id",
    "lead_id",
    "user_id",
    "customer_id",
    "record_id",
}


def build_trend_plan(
    df,
    x: str,
    y: str,
    *,
    frequency: str = "day",
    analysis_type: str = "time_series",
):

    # --------------------------------------------------
    # Validate columns
    # --------------------------------------------------

    if x not in df.columns:
        raise ValueError(
            f"Column '{x}' does not exist."
        )

    if y not in df.columns:
        raise ValueError(
            f"Column '{y}' does not exist."
        )

    # --------------------------------------------------
    # Determine time column
    # --------------------------------------------------

    if is_datetime64_any_dtype(df[x]):

        time_column = x
        metric = y

    elif is_datetime64_any_dtype(df[y]):

        time_column = y
        metric = x

    else:

        raise ValueError(
            "Trend analysis requires "
            "one datetime column."
        )

    # --------------------------------------------------
    # Determine aggregation
    # --------------------------------------------------

    metric_lower = metric.lower()

    if metric_lower in IDENTIFIER_COLUMNS:

        aggregation = "count"

    elif not is_numeric_dtype(df[metric]):

        aggregation = "count"

    else:

        aggregation = "mean"

    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    if aggregation == "count":

        statistics = [
            "count",
        ]

    else:

        statistics = [
            "count",
            "mean",
            "min",
            "max",
        ]

    # --------------------------------------------------
    # Build plan
    # --------------------------------------------------

    plan = TrendPlan(
        x=x,
        y=y,

        analysis_type=analysis_type,

        time_column=time_column,
        metric=metric,

        aggregation=aggregation,

        statistics=statistics,

        chart_type="line",

        frequency=frequency,
    )

    # --------------------------------------------------
    # DEBUG
    # --------------------------------------------------

    print(
        "[TREND PLANNER]"
    )

    print(
        f"  time_column = {plan.time_column}"
    )

    print(
        f"  metric      = {plan.metric}"
    )

    print(
        f"  aggregation = {plan.aggregation}"
    )

    print(
        f"  frequency   = {plan.frequency}"
    )

    return plan