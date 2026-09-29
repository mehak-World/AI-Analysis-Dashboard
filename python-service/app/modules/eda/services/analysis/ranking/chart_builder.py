"""
Builds a ChartSpec for ranking analysis.

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

    sort_order = (
        SortOrder.ASC
        if plan.order == "asc"
        else SortOrder.DESC
    )

    if plan.analysis_type == "ranking_by_count":

        return ChartSpec(
            name=f"Ranking of {plan.category} by count",
            reason="Ranking analysis",
            chart_type=ChartType.BAR,
            x=Axis(column=plan.category, label=plan.category),
            y=Axis(column=plan.category, label="Count"),
            aggregation=Aggregation.COUNT,
            sort=sort_order,
            limit=plan.top_n,
        )

    if plan.analysis_type == "ranking_by_value":

        return ChartSpec(
            name=f"Ranking of {plan.category} by {plan.value}",
            reason="Ranking analysis",
            chart_type=ChartType.BAR,
            x=Axis(column=plan.category, label=plan.category),
            y=Axis(column=plan.value, label=plan.value),
            aggregation=Aggregation.SUM,
            sort=sort_order,
            limit=plan.top_n,
        )

    raise ValueError(f"Unsupported analysis type '{plan.analysis_type}'.")