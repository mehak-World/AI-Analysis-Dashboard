"""
Relationship analysis planner.

Determines the best statistical analysis and visualization
based on the datatypes of two columns.

No AI is used here.
"""

from pandas.api.types import (
    is_numeric_dtype,
    is_bool_dtype,
    is_datetime64_any_dtype,
)

from .models import RelationshipPlan


def build_relationship_plan(
    df,
    x: str,
    y: str,
) -> RelationshipPlan:
    """
    Returns a RelationshipPlan for two dataset columns.
    """

    x_series = df[x]
    y_series = df[y]

    x_numeric = is_numeric_dtype(x_series)
    y_numeric = is_numeric_dtype(y_series)

    x_datetime = is_datetime64_any_dtype(x_series)
    y_datetime = is_datetime64_any_dtype(y_series)

    x_bool = is_bool_dtype(x_series)
    y_bool = is_bool_dtype(y_series)

    # Treat booleans as categorical
    x_categorical = (
        not x_numeric
        or x_bool
    )

    y_categorical = (
        not y_numeric
        or y_bool
    )

    # ------------------------------
    # Numeric vs Numeric
    # ------------------------------

    if x_numeric and y_numeric:

        return RelationshipPlan(
            x=x,
            y=y,
            analysis_type="correlation",
            chart_type="scatter",
            statistics=[
                "pearson",
                "spearman",
                "covariance",
            ],
        )

    # ------------------------------
    # Numeric vs Category
    # ------------------------------

    if x_numeric and y_categorical:
        return RelationshipPlan(
            x=x,
            y=y,
            analysis_type="group_comparison",
            chart_type="box",
            statistics=[
                "mean",
                "median",
                "std",
                "count",
            ],
        )

    # ------------------------------
    # Category vs Numeric
    # ------------------------------

    if x_categorical and y_numeric:

        return RelationshipPlan(
            x=x,
            y=y,
            analysis_type="group_comparison",
            chart_type="box",
            statistics=[
                "mean",
                "median",
                "std",
                "count",
            ],
        )

    # ------------------------------
    # Category vs Category
    # ------------------------------

    if x_categorical and y_categorical:

        return RelationshipPlan(
            x=x,
            y=y,
            analysis_type="association",
            chart_type="stacked_bar",
            statistics=[
                "crosstab",
                "chi_square",
                "cramers_v",
            ],
        )

    # ------------------------------
    # Time vs Numeric
    # ------------------------------

    if x_datetime and y_numeric:

        return RelationshipPlan(
            x=x,
            y=y,
            analysis_type="trend",
            chart_type="line",
            statistics=[
                "rolling_mean",
            ],
        )

    if y_datetime and x_numeric:

        return RelationshipPlan(
            x=x,
            y=y,
            analysis_type="trend",
            chart_type="line",
            statistics=[
                "rolling_mean",
            ],
        )

    raise ValueError(
        f"Unsupported relationship between '{x}' and '{y}'."
    )