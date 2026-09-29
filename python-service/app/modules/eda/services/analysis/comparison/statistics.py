"""
Comparison statistics engine.

Computes the statistical evidence required by
a ComparisonPlan.

No AI is used here.
"""

import pandas as pd


def generate_comparison_statistics(
    df: pd.DataFrame,
    plan,
) -> dict:

    if plan.comparison_type == "numeric_by_category":
        return _numeric_by_category(
            df,
            plan,
        )

    if plan.comparison_type == "rate_by_category":
        return _rate_by_category(
            df,
            plan,
        )

    raise ValueError(
        f"Unsupported comparison type "
        f"'{plan.comparison_type}'."
    )


# ---------------------------------------------------
# Numeric by Category
# ---------------------------------------------------

def _numeric_by_category(
    df: pd.DataFrame,
    plan,
) -> dict:

    metric = plan.metric
    group = plan.group

    data = df[[group, metric]].copy()

    # Remove rows where either value is missing.
    data = data.dropna(
        subset=[group, metric]
    )

    grouped = (
        data
        .groupby(group)[metric]
        .agg(
            count="count",
            mean="mean",
            median="median",
            std="std",
            min="min",
            max="max",
        )
        .reset_index()
    )

    grouped = grouped.round(2)

    groups = grouped.to_dict(
        orient="records"
    )

    # Determine highest and lowest groups
    # based on the mean.
    if groups:

        highest = max(
            groups,
            key=lambda row: row["mean"],
        )

        lowest = min(
            groups,
            key=lambda row: row["mean"],
        )

        difference = (
            highest["mean"]
            - lowest["mean"]
        )

    else:

        highest = None
        lowest = None
        difference = None

    return {
        "comparison_type": "numeric_by_category",

        "metric": metric,
        "group": group,

        "groups": groups,

        "highest_group": highest,
        "lowest_group": lowest,

        "difference": (
            round(difference, 2)
            if difference is not None
            else None
        ),

        "sample_size": len(data),
    }


# ---------------------------------------------------
# Rate by Category
# ---------------------------------------------------

def _rate_by_category(
    df: pd.DataFrame,
    plan,
) -> dict:

    group = plan.group
    outcome = plan.outcome

    data = df[[group, outcome]].copy()

    # Remove rows where either value is missing.
    data = data.dropna(
        subset=[group, outcome]
    )

    # Determine the positive outcome.
    positive_value = _detect_positive_value(
        data[outcome]
    )

    # Count total observations per group.
    total = (
        data
        .groupby(group)
        .size()
        .rename("count")
    )

    # Count positive observations per group.
    positive = (
        data[outcome] == positive_value
    )

    positive_count = (
        positive
        .groupby(data[group])
        .sum()
        .rename("positive_count")
    )

    result = pd.concat(
        [
            total,
            positive_count,
        ],
        axis=1,
    ).reset_index()

    # Calculate rate.
    result["rate"] = (
        result["positive_count"]
        / result["count"]
    )

    result["rate"] = (
        result["rate"]
        .round(4)
    )

    groups = result.to_dict(
        orient="records"
    )

    # Determine highest and lowest groups.
    if groups:

        highest = max(
            groups,
            key=lambda row: row["rate"],
        )

        lowest = min(
            groups,
            key=lambda row: row["rate"],
        )

        difference = (
            highest["rate"]
            - lowest["rate"]
        )

    else:

        highest = None
        lowest = None
        difference = None

    return {
        "comparison_type": "rate_by_category",

        "group": group,
        "outcome": outcome,

        "positive_value": positive_value,

        "groups": groups,

        "highest_group": highest,
        "lowest_group": lowest,

        "difference": (
            round(difference, 4)
            if difference is not None
            else None
        ),

        "sample_size": len(data),
    }


# ---------------------------------------------------
# Positive Outcome Detection
# ---------------------------------------------------

def _detect_positive_value(
    series: pd.Series,
):
    """
    Detect the value that represents a positive
    outcome for rate calculations.

    Handles common boolean / binary categorical
    representations.
    """

    values = series.dropna().unique().tolist()

    if not values:
        raise ValueError(
            "Cannot determine positive outcome "
            "from an empty column."
        )

    # Boolean
    if series.dtype == bool:
        return True

    # Numeric binary
    if set(values).issubset({0, 1}):
        return 1

    # Common string representations
    normalized = {
        str(value).strip().lower(): value
        for value in values
    }

    positive_candidates = [
        "yes",
        "true",
        "approved",
        "accepted",
        "success",
        "successful",
        "converted",
        "positive",
        "pass",
        "passed",
        "1",
    ]

    for candidate in positive_candidates:

        if candidate in normalized:
            return normalized[candidate]

    # If there are exactly two categories and
    # no known positive label exists, fail rather
    # than silently choosing the wrong one.
    if len(values) == 2:

        raise ValueError(
            f"Unable to determine the positive "
            f"outcome for column '{series.name}'. "
            f"Values found: {values}"
        )

    raise ValueError(
        f"Rate comparison requires a binary "
        f"outcome column. Values found: {values}"
    )