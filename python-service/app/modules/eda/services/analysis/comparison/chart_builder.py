"""
Builds a ChartSpec for comparison analysis.

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


def build_chart_spec(plan, statistics=None,):

    # --------------------------------------------------
    # Numeric by Category
    # --------------------------------------------------

    if plan.comparison_type == "numeric_by_category":

        return ChartSpec(
            name=f"{plan.metric} by {plan.group}",
            reason="Comparison analysis",

            chart_type=ChartType.BAR,

            x=Axis(
                column=plan.group,
                label=plan.group,
            ),

            y=Axis(
                column=plan.metric,
                label=plan.metric,
            ),

            aggregation=Aggregation.MEAN,

            sort=SortOrder.DESC,
        )

    # --------------------------------------------------
    # Rate by Category
    # --------------------------------------------------
    if plan.comparison_type == "rate_by_category":

        positive_value = (
            statistics.get("positive_value")
            if statistics
            else None
        )

        return ChartSpec(
            name=f"{plan.outcome} rate by {plan.group}",
            reason="Comparison analysis",

            chart_type=ChartType.BAR,

            x=Axis(
                column=plan.group,
                label=plan.group,
            ),

            y=Axis(
                column=plan.outcome,
                label=f"{plan.outcome} Rate",
                unit="%",
            ),

            aggregation=Aggregation.COUNT,

            sort=SortOrder.DESC,

            options={
                "metric": "rate",
                "positive_value": positive_value,
            },
        )

    raise ValueError(
        f"Unsupported comparison type "
        f"'{plan.comparison_type}'."
    )