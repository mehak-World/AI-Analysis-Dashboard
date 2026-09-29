"""
Ranking statistics engine.

Computes the statistical evidence required for
a RankingPlan.
"""

import pandas as pd


def generate_ranking_statistics(
    df: pd.DataFrame,
    plan,
) -> dict:

    if plan.analysis_type == "ranking_by_count":
        return _ranking_by_count(df, plan)

    if plan.analysis_type == "ranking_by_value":
        return _ranking_by_value(df, plan)

    raise ValueError(
        f"Unsupported analysis '{plan.analysis_type}'."
    )


# ---------------------------------------------------
# Ranking by count
# ---------------------------------------------------

def _ranking_by_count(
    df,
    plan,
):

    counts = df[plan.category].value_counts()

    total = int(counts.sum())

    ascending = plan.order == "asc"

    counts = counts.sort_values(ascending=ascending)

    ranked = counts.head(plan.top_n)

    rows = [
        {
            "rank": i + 1,
            "category": str(index),
            "value": int(count),
            "share_of_total": round(float(count / total * 100), 2) if total else 0,
        }
        for i, (index, count) in enumerate(ranked.items())
    ]

    return {
        "category_column": plan.category,
        "value_column": "count",
        "total": total,
        "unique_categories": int(df[plan.category].nunique()),
        "ranked": rows,
    }


# ---------------------------------------------------
# Ranking by aggregated value
# ---------------------------------------------------

def _ranking_by_value(
    df,
    plan,
):

    grouped = (
        df.groupby(plan.category)[plan.value]
        .sum()
        .round(4)
    )

    total = float(grouped.sum())

    ascending = plan.order == "asc"

    grouped = grouped.sort_values(ascending=ascending)

    ranked = grouped.head(plan.top_n)

    rows = [
        {
            "rank": i + 1,
            "category": str(index),
            "value": float(value),
            "share_of_total": round(float(value / total * 100), 2) if total else 0,
        }
        for i, (index, value) in enumerate(ranked.items())
    ]

    return {
        "category_column": plan.category,
        "value_column": plan.value,
        "total": round(total, 4),
        "unique_categories": int(df[plan.category].nunique()),
        "ranked": rows,
    }