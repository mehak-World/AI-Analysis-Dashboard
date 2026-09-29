"""
Builds a ChartSpec for trend analysis.

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

    aggregation_map = {
        "count": Aggregation.COUNT,
        "mean": Aggregation.MEAN,
        "sum": Aggregation.SUM,
        "min": Aggregation.MIN,
        "max": Aggregation.MAX,
        "median": Aggregation.MEDIAN,
    }

    aggregation = aggregation_map.get(
        plan.aggregation
    )

    if aggregation is None:
        raise ValueError(
            f"Unsupported aggregation "
            f"'{plan.aggregation}'."
        )

    return ChartSpec(

        name=(
            f"{plan.metric} "
            f"{plan.aggregation} "
            f"over {plan.time_column}"
        ),

        reason="Trend analysis",

        chart_type=ChartType.LINE,

        x=Axis(
            column=plan.time_column,
            label=plan.time_column,
        ),

        y=Axis(
            column=plan.metric,
            label=(
                "Lead Count"
                if plan.aggregation == "count"
                else plan.metric
            ),
        ),

        aggregation=aggregation,

        sort=SortOrder.ASC,

        options={
            "frequency": plan.frequency,
            "metric": plan.aggregation,
        },
    )