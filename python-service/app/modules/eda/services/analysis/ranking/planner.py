"""
Ranking analysis planner.

Determines how to rank a categorical column, either by
frequency (count) or by an aggregated numeric value.

No AI is used here.
"""

from pandas.api.types import (
    is_numeric_dtype,
    is_bool_dtype,
)

from .models import RankingPlan

DEFAULT_TOP_N = 10


def build_ranking_plan(
    df,
    category: str,
    value: str | None = None,
    top_n: int = DEFAULT_TOP_N,
    order: str = "desc",
) -> RankingPlan:
    """
    Returns a RankingPlan.

    If `value` is None or not numeric, ranking falls back
    to frequency count of the category column.
    """

    category_series = df[category]

    if category_series.nunique() == 0:
        raise ValueError(
            f"Column '{category}' has no values to rank."
        )

    # ------------------------------
    # Ranking by count (frequency)
    # ------------------------------

    if value is None:

        return RankingPlan(
            category=category,
            value=None,
            analysis_type="ranking_by_count",
            chart_type="bar",
            aggregation="count",
            order=order,
            top_n=top_n,
            statistics=[
                "value_counts",
                "share_of_total",
            ],
        )

    value_series = df[value]

    value_numeric = (
        is_numeric_dtype(value_series)
        and not is_bool_dtype(value_series)
    )

    # ------------------------------
    # Ranking by aggregated value
    # ------------------------------

    if value_numeric:

        return RankingPlan(
            category=category,
            value=value,
            analysis_type="ranking_by_value",
            chart_type="bar",
            aggregation="sum",
            order=order,
            top_n=top_n,
            statistics=[
                "grouped_sum",
                "share_of_total",
            ],
        )

    # ------------------------------
    # Value given but not numeric -> fall back to count
    # ------------------------------

    return RankingPlan(
        category=category,
        value=None,
        analysis_type="ranking_by_count",
        chart_type="bar",
        aggregation="count",
        order=order,
        top_n=top_n,
        statistics=[
            "value_counts",
            "share_of_total",
        ],
    )