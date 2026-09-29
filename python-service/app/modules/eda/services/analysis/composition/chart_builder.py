from app.modules.eda.services.charts.models import (
    Aggregation,
    Axis,
    ChartSpec,
    ChartType,
    SortOrder,
)


def build_chart_spec(plan):

    # -----------------------------
    # Share of count
    # -----------------------------

    if plan.analysis_type == "composition_by_count":

        return ChartSpec(
            name=f"Composition of {plan.category}",
            reason="Composition analysis",
            chart_type=ChartType.BAR,
            x=Axis(column=plan.category, label=plan.category),
            y=Axis(column=plan.category, label="Count"),
            aggregation=Aggregation.COUNT,
            sort=SortOrder.DESC,
            limit=plan.max_slices,
        )

    # -----------------------------
    # Share of summed value
    # -----------------------------

    if plan.analysis_type == "composition_by_value":

        return ChartSpec(
            name=f"Composition of {plan.category} by {plan.value}",
            reason="Composition analysis",
            chart_type=ChartType.BAR,
            x=Axis(column=plan.category, label=plan.category),
            y=Axis(column=plan.value, label=plan.value),
            aggregation=Aggregation.SUM,
            sort=SortOrder.DESC,
            limit=plan.max_slices,
        )

    # -----------------------------
    # Hierarchical -> heatmap (no treemap type available)
    # -----------------------------

    if plan.analysis_type == "composition_hierarchical":

        return ChartSpec(
            name=f"Composition of {plan.category} by {plan.subcategory}",
            reason="Composition analysis",
            chart_type=ChartType.HEATMAP,
            x=Axis(column=plan.category, label=plan.category),
            y=Axis(column=plan.subcategory, label=plan.subcategory),
            aggregation=Aggregation.COUNT,
            sort=SortOrder.DESC,
        )

    raise ValueError(f"Unsupported analysis type '{plan.analysis_type}'.")