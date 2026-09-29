"""
Distribution analysis planner.

Determines the best statistical analysis and visualization
based on the datatype of a single column.

No AI is used here.
"""

from pandas.api.types import (
    is_numeric_dtype,
    is_bool_dtype,
    is_datetime64_any_dtype,
)

from .models import DistributionPlan


def build_distribution_plan(
    df,
    column: str,
) -> DistributionPlan:
    """
    Returns a DistributionPlan for a single dataset column.
    """

    series = df[column]

    is_numeric = is_numeric_dtype(series)
    is_bool = is_bool_dtype(series)
    is_datetime = is_datetime64_any_dtype(series)

    # Treat booleans as categorical
    is_categorical = (
        not is_numeric
        or is_bool
    )

    # ------------------------------
    # Numeric
    # ------------------------------

    if is_numeric and not is_bool:

        return DistributionPlan(
            column=column,
            analysis_type="numeric_distribution",
            chart_type="histogram",
            statistics=[
                "mean",
                "median",
                "std",
                "skewness",
                "kurtosis",
                "percentiles",
                "outliers",
            ],
        )

    # ------------------------------
    # Categorical / Boolean
    # ------------------------------

    if is_categorical and not is_datetime:

        return DistributionPlan(
            column=column,
            analysis_type="categorical_distribution",
            chart_type="bar",
            statistics=[
                "value_counts",
                "mode",
                "unique_count",
            ],
        )

    raise ValueError(
        f"Unsupported distribution for column '{column}'."
    )