"""
Builds a ChartSpec for distribution analysis.

This module does NOT generate charts.
It only constructs a ChartSpec that is later
passed to generate_charts().
"""

from app.modules.eda.services.charts.models import (
    Aggregation,
    Axis,
    ChartSpec,
    ChartType,
    SortOrder,
)


def build_chart_spec(plan):

    # -----------------------------
    # Numeric distribution
    # -----------------------------

    if plan.analysis_type == "numeric_distribution":

        return ChartSpec(
            name=f"Distribution of {plan.column}",
            reason="Distribution analysis",

            chart_type=ChartType.HISTOGRAM,

            x=Axis(
                column=plan.column,
                label=plan.column,
            ),

            y=None,

            aggregation=Aggregation.NONE,
            sort=SortOrder.NONE,
        )

    # -----------------------------
    # Categorical distribution
    # -----------------------------

    if plan.analysis_type == "categorical_distribution":

        return ChartSpec(
            name=f"Distribution of {plan.column}",
            reason="Distribution analysis",

            chart_type=ChartType.BAR,

            x=Axis(
                column=plan.column,
                label=plan.column,
            ),

            y=Axis(
                column=plan.column,
                label="Count",
            ),

            aggregation=Aggregation.COUNT,
            sort=SortOrder.DESC,
        )

    raise ValueError(
        f"Unsupported analysis type '{plan.analysis_type}'."
    )