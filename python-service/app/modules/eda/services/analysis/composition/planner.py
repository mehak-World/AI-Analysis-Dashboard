"""
Composition analysis planner.

Determines how to break a whole down into parts:
- single category -> share of count
- category + numeric value -> share of a summed metric
- category + subcategory -> hierarchical (treemap) composition

No AI is used here.
"""

from pandas.api.types import (
    is_numeric_dtype,
    is_bool_dtype,
)

from .models import CompositionPlan

DEFAULT_MAX_SLICES = 8


def build_composition_plan(
    df,
    category: str,
    second_entity: str | None = None,
    max_slices: int = DEFAULT_MAX_SLICES,
) -> CompositionPlan:

    if df[category].nunique() == 0:
        raise ValueError(
            f"Column '{category}' has no values to compose."
        )

    # ------------------------------
    # No second entity -> simple share of count
    # ------------------------------

    if second_entity is None:

        return CompositionPlan(
            category=category,
            subcategory=None,
            value=None,
            analysis_type="composition_by_count",
            chart_type="pie",
            max_slices=max_slices,
            statistics=[
                "value_counts",
                "share_of_total",
            ],
        )

    second_series = df[second_entity]

    second_numeric = (
        is_numeric_dtype(second_series)
        and not is_bool_dtype(second_series)
    )

    # ------------------------------
    # category + numeric value -> share of summed metric
    # ------------------------------

    if second_numeric:

        return CompositionPlan(
            category=category,
            subcategory=None,
            value=second_entity,
            analysis_type="composition_by_value",
            chart_type="pie",
            max_slices=max_slices,
            statistics=[
                "grouped_sum",
                "share_of_total",
            ],
        )

    # ------------------------------
    # category + categorical -> hierarchical composition
    # ------------------------------

    return CompositionPlan(
        category=category,
        subcategory=second_entity,
        value=None,
        analysis_type="composition_hierarchical",
        chart_type="treemap",
        max_slices=max_slices,
        statistics=[
            "hierarchical_counts",
        ],
    )