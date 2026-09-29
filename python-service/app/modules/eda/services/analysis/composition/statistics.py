"""
Composition statistics engine.

Computes the statistical evidence required for
a CompositionPlan, including "Other" bucketing so
pie/treemap charts stay readable with high-cardinality
categories.
"""

import pandas as pd


def generate_composition_statistics(
    df: pd.DataFrame,
    plan,
) -> dict:

    if plan.analysis_type == "composition_by_count":
        return _composition_by_count(df, plan)

    if plan.analysis_type == "composition_by_value":
        return _composition_by_value(df, plan)

    if plan.analysis_type == "composition_hierarchical":
        return _composition_hierarchical(df, plan)

    raise ValueError(
        f"Unsupported analysis '{plan.analysis_type}'."
    )


def _bucket_other(rows, max_slices, value_key="value"):
    """
    Keeps the top (max_slices - 1) rows and folds the rest
    into a single "Other" row, so charts don't blow up with
    30+ slices.
    """

    if len(rows) <= max_slices:
        return rows

    kept = rows[: max_slices - 1]
    rest = rows[max_slices - 1:]

    other_value = sum(r[value_key] for r in rest)
    other_share = round(sum(r["share_of_total"] for r in rest), 2)

    kept.append({
        "category": "Other",
        value_key: other_value,
        "share_of_total": other_share,
    })

    return kept


# ---------------------------------------------------
# Single category, share of count
# ---------------------------------------------------

def _composition_by_count(
    df,
    plan,
):

    counts = df[plan.category].value_counts()
    total = int(counts.sum())

    rows = [
        {
            "category": str(index),
            "value": int(count),
            "share_of_total": round(float(count / total * 100), 2) if total else 0,
        }
        for index, count in counts.items()
    ]

    rows.sort(key=lambda r: r["value"], reverse=True)

    rows = _bucket_other(rows, plan.max_slices)

    return {
        "category_column": plan.category,
        "value_column": "count",
        "total": total,
        "unique_categories": int(df[plan.category].nunique()),
        "parts": rows,
    }


# ---------------------------------------------------
# Category + numeric value, share of summed metric
# ---------------------------------------------------

def _composition_by_value(
    df,
    plan,
):

    grouped = (
        df.groupby(plan.category)[plan.value]
        .sum()
        .round(4)
    )

    total = float(grouped.sum())

    rows = [
        {
            "category": str(index),
            "value": float(value),
            "share_of_total": round(float(value / total * 100), 2) if total else 0,
        }
        for index, value in grouped.items()
    ]

    rows.sort(key=lambda r: r["value"], reverse=True)

    rows = _bucket_other(rows, plan.max_slices)

    return {
        "category_column": plan.category,
        "value_column": plan.value,
        "total": round(total, 4),
        "unique_categories": int(df[plan.category].nunique()),
        "parts": rows,
    }


# ---------------------------------------------------
# Hierarchical: category -> subcategory counts
# ---------------------------------------------------

def _composition_hierarchical(
    df,
    plan,
):

    grouped = (
        df.groupby([plan.category, plan.subcategory])
        .size()
        .reset_index(name="count")
    )

    total = int(grouped["count"].sum())

    tree = {}

    for _, row in grouped.iterrows():
        parent = str(row[plan.category])
        child = str(row[plan.subcategory])
        count = int(row["count"])

        tree.setdefault(parent, []).append({
            "subcategory": child,
            "value": count,
            "share_of_total": round(float(count / total * 100), 2) if total else 0,
        })

    parts = [
        {
            "category": parent,
            "children": sorted(
                children,
                key=lambda c: c["value"],
                reverse=True,
            ),
            "value": sum(c["value"] for c in children),
        }
        for parent, children in tree.items()
    ]

    parts.sort(key=lambda p: p["value"], reverse=True)

    return {
        "category_column": plan.category,
        "subcategory_column": plan.subcategory,
        "total": total,
        "unique_categories": int(df[plan.category].nunique()),
        "unique_subcategories": int(df[plan.subcategory].nunique()),
        "parts": parts,
    }