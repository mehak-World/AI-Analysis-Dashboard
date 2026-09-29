"""
Comparison analysis planner.

Determines the appropriate comparison analysis
based on the datatypes of two dataset columns.

No AI is used here.
"""

from pandas.api.types import (
    is_numeric_dtype,
    is_bool_dtype,
    is_datetime64_any_dtype,
)

from .models import ComparisonPlan

def _is_binary_outcome(series) -> bool:

    values = series.dropna().unique().tolist()

    if len(values) != 2:
        return False

    # Boolean
    if series.dtype == bool:
        return True

    # Numeric binary
    if set(values).issubset({0, 1}):
        return True

    normalized = {
        str(value).strip().lower()
        for value in values
    }

    outcome_values = {
        "yes",
        "no",
        "true",
        "false",
        "approved",
        "rejected",
        "accepted",
        "declined",
        "success",
        "failure",
        "successful",
        "unsuccessful",
        "converted",
        "not converted",
        "positive",
        "negative",
        "pass",
        "fail",
        "passed",
        "failed",
        "1",
        "0",
    }

    return normalized.issubset(outcome_values)


def build_comparison_plan(
    df,
    x: str,
    y: str,
) -> ComparisonPlan:
    """
    Build a comparison plan for two dataset columns.
    """

    if x not in df.columns:
        raise ValueError(
            f"Column '{x}' does not exist in the dataset."
        )

    if y not in df.columns:
        raise ValueError(
            f"Column '{y}' does not exist in the dataset."
        )

    x_series = df[x]
    y_series = df[y]

    x_numeric = is_numeric_dtype(x_series)
    y_numeric = is_numeric_dtype(y_series)

    x_datetime = is_datetime64_any_dtype(x_series)
    y_datetime = is_datetime64_any_dtype(y_series)

    x_bool = is_bool_dtype(x_series)
    y_bool = is_bool_dtype(y_series)

    # Boolean is treated as categorical.
    x_categorical = (
        not x_numeric
        and not x_datetime
    ) or x_bool

    y_categorical = (
        not y_numeric
        and not y_datetime
    ) or y_bool

    # --------------------------------------------------
    # Numeric × Category
    # --------------------------------------------------

    if x_numeric and y_categorical:

        return ComparisonPlan(
            x=x,
            y=y,
            comparison_type="numeric_by_category",
            metric=x,
            group=y,
            statistics=[
                "count",
                "mean",
                "median",
                "std",
                "min",
                "max",
            ],
            chart_type="bar",
        )

    # --------------------------------------------------
    # Category × Numeric
    # --------------------------------------------------

    if x_categorical and y_numeric:

        return ComparisonPlan(
            x=x,
            y=y,
            comparison_type="numeric_by_category",
            metric=y,
            group=x,
            statistics=[
                "count",
                "mean",
                "median",
                "std",
                "min",
                "max",
            ],
            chart_type="bar",
        )

    # --------------------------------------------------
    # Category × Category
    # --------------------------------------------------
    # --------------------------------------------------
# Category × Category
# --------------------------------------------------

    if x_categorical and y_categorical:

        x_is_outcome = _is_binary_outcome(df[x])
        y_is_outcome = _is_binary_outcome(df[y])

        if x_is_outcome and not y_is_outcome:

            group = y
            outcome = x

        elif y_is_outcome and not x_is_outcome:

            group = x
            outcome = y

        elif x_is_outcome and y_is_outcome:

            raise ValueError(
                f"Both '{x}' and '{y}' appear to be "
                "binary outcome columns. Unable to determine "
                "which column should be the grouping variable."
            )

        else:

            raise ValueError(
                f"Neither '{x}' nor '{y}' appears to be a "
                "binary outcome column required for rate comparison."
            )

        return ComparisonPlan(
                x=x,
                y=y,
                comparison_type="rate_by_category",
                group=group,
                outcome=outcome,
                statistics=[
                    "count",
                    "positive_count",
                    "rate",
                ],
                chart_type="bar",
            )

    # --------------------------------------------------
    # Unsupported
    # --------------------------------------------------

    raise ValueError(
        f"Unsupported comparison between "
        f"'{x}' and '{y}'."
    )