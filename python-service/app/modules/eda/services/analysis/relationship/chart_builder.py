"""
Builds a ChartSpec for relationship analysis.

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
    # Correlation
    # -----------------------------

    if plan.analysis_type == "correlation":

        return ChartSpec(
            name=f"{plan.x} vs {plan.y}",
            reason="Relationship analysis",

            chart_type=ChartType.SCATTER,

            x=Axis(
                column=plan.x,
                label=plan.x,
            ),

            y=Axis(
                column=plan.y,
                label=plan.y,
            ),

            aggregation=Aggregation.NONE,
            sort=SortOrder.NONE,
        )

    # -----------------------------
    # Numeric vs Category
    # -----------------------------

    if plan.analysis_type == "group_comparison":

        return ChartSpec(
            name=f"{plan.x} by {plan.y}",
            reason="Relationship analysis",

            chart_type=ChartType.BOXPLOT,

            x=Axis(
                column=plan.y,
                label=plan.y,
            ),

            y=Axis(
                column=plan.x,
                label=plan.x,
            ),

            aggregation=Aggregation.NONE,
            sort=SortOrder.NONE,
        )

    # -----------------------------
    # Category vs Category
    # -----------------------------

    if plan.analysis_type == "association":

        return ChartSpec(
            name=f"{plan.x} vs {plan.y}",
            reason="Relationship analysis",

            chart_type=ChartType.BAR,

            x=Axis(
                column=plan.x,
                label=plan.x,
            ),

            y=Axis(
                column=plan.y,
                label=plan.y,
            ),

            aggregation=Aggregation.COUNT,
            sort=SortOrder.NONE,

            options={
                "stacked": True,
            },
        )

    # -----------------------------
    # Time Series
    # -----------------------------

    if plan.analysis_type == "trend":

        return ChartSpec(
            name=f"{plan.y} over {plan.x}",
            reason="Relationship analysis",

            chart_type=ChartType.LINE,

            x=Axis(
                column=plan.x,
                label=plan.x,
            ),

            y=Axis(
                column=plan.y,
                label=plan.y,
            ),

            aggregation=Aggregation.MEAN,
            sort=SortOrder.ASC,
        )

    raise ValueError(
        f"Unsupported analysis type '{plan.analysis_type}'."
    )