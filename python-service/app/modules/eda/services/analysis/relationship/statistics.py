"""
Relationship statistics engine.

Computes the statistical evidence required for
a RelationshipPlan.
"""

import pandas as pd

from scipy.stats import (
    pearsonr,
    spearmanr,
    chi2_contingency,
)


def generate_relationship_statistics(
    df: pd.DataFrame,
    plan,
) -> dict:

    if plan.analysis_type == "correlation":
        return _correlation(df, plan)

    if plan.analysis_type == "group_comparison":
        return _group_comparison(df, plan)

    if plan.analysis_type == "association":
        return _association(df, plan)

    if plan.analysis_type == "trend":
        return _trend(df, plan)

    raise ValueError(
        f"Unsupported analysis '{plan.analysis_type}'."
    )


# ---------------------------------------------------
# Numeric vs Numeric
# ---------------------------------------------------

def _correlation(
    df,
    plan,
):

    x = df[plan.x]
    y = df[plan.y]

    pearson, _ = pearsonr(x, y)
    spearman, _ = spearmanr(x, y)

    return {
        "pearson": round(float(pearson), 4),
        "spearman": round(float(spearman), 4),
        "count": len(df),
    }


# ---------------------------------------------------
# Numeric vs Category
# ---------------------------------------------------

def _group_comparison(
    df,
    plan,
):

    numeric = plan.x
    category = plan.y

    if not pd.api.types.is_numeric_dtype(df[numeric]):
        numeric, category = category, numeric

    grouped = (
        df.groupby(category)[numeric]
        .agg([
            "count",
            "mean",
            "median",
            "std",
            "min",
            "max",
        ])
        .round(2)
    )

    return {
        "groups": grouped.reset_index().to_dict("records"),
    }


# ---------------------------------------------------
# Category vs Category
# ---------------------------------------------------

def _association(
    df,
    plan,
):

    table = pd.crosstab(
        df[plan.x],
        df[plan.y],
    )

    chi2, p, _, _ = chi2_contingency(table)

    return {
        "chi_square": round(float(chi2), 4),
        "p_value": round(float(p), 6),
        "crosstab": table.reset_index().to_dict("records"),
    }


# ---------------------------------------------------
# Time Series
# ---------------------------------------------------

def _trend(
    df,
    plan,
):

    numeric = plan.y
    time = plan.x

    if pd.api.types.is_numeric_dtype(df[time]):
        numeric, time = time, numeric

    trend = (
        df.sort_values(time)
        .groupby(time)[numeric]
        .mean()
        .reset_index()
    )

    return {
        "trend": trend.to_dict("records"),
    }