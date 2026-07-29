"""
Candidate chart generation.

Given semantic roles + correlations, enumerates every chart that is
*structurally valid* — e.g. don't bar-chart an identifier, don't
pie-chart a 200-category column, don't scatter-plot two unrelated
measures. Business relevance ranking happens later in scorer.py;
this stage only filters out charts that would be nonsensical, ugly,
or broken.
"""
from typing import List

import pandas as pd

from .models import Aggregation, Axis, ChartSpec, ChartType, SortOrder
from .semantic_roles import ColumnRole, SemanticRole

MAX_BAR_CARDINALITY = 20
MAX_PIE_CARDINALITY = 8
MIN_DIMENSION_CARDINALITY = 2
MAX_NULL_PERCENT = 40.0
MIN_CORRELATION_FOR_SCATTER = 0.3


def generate_candidates(
    roles: List[ColumnRole],
    correlations: List[dict],
) -> List[ChartSpec]:

    measures = [
        r for r in roles
        if r.role == SemanticRole.MEASURE
        and r.null_percent <= MAX_NULL_PERCENT
    ]
    dimensions = [
        r for r in roles
        if r.role == SemanticRole.DIMENSION
        and MIN_DIMENSION_CARDINALITY <= r.cardinality <= MAX_BAR_CARDINALITY
        and r.null_percent <= MAX_NULL_PERCENT
    ]
    small_dimensions = [d for d in dimensions if d.cardinality <= MAX_PIE_CARDINALITY]
    datetimes = [r for r in roles if r.role == SemanticRole.DATETIME]
    booleans = [
        r for r in roles
        if r.role == SemanticRole.BOOLEAN_FLAG
        and r.null_percent <= MAX_NULL_PERCENT
    ]

    candidates: List[ChartSpec] = []
    candidates += _measure_by_dimension_bars(measures, dimensions)
    candidates += _measure_over_time_lines(measures, datetimes)
    candidates += _dimension_distributions(small_dimensions + booleans)
    candidates += _measure_distributions(measures)
    candidates += _correlation_scatters(correlations, measures)
    candidates += _correlation_heatmap(measures)
    return candidates


def _label(name: str) -> str:
    return name.replace("_", " ").replace("-", " ").title()


def _measure_by_dimension_bars(measures, dimensions) -> List[ChartSpec]:
    specs = []
    for measure in measures:
        for dim in dimensions:
            specs.append(ChartSpec(
                name=f"{measure.name}_by_{dim.name}",
                chart_type=ChartType.BAR,
                x=Axis(column=dim.name, label=_label(dim.name)),
                y=Axis(column=measure.name, label=_label(measure.name), unit=measure.unit),
                aggregation=Aggregation.SUM,
                sort=SortOrder.DESC,
                reason=(
                    f"Shows total {measure.name} broken down by {dim.name}, "
                    f"useful for spotting which {dim.name} drives the most "
                    f"{measure.name}."
                ),
                options={"dimension_cardinality": dim.cardinality},
            ))
            # Mean variant surfaces per-unit performance, not just volume.
            specs.append(ChartSpec(
                name=f"avg_{measure.name}_by_{dim.name}",
                chart_type=ChartType.BAR,
                x=Axis(column=dim.name, label=_label(dim.name)),
                y=Axis(column=measure.name, label=f"Avg {_label(measure.name)}", unit=measure.unit),
                aggregation=Aggregation.MEAN,
                sort=SortOrder.DESC,
                reason=(
                    f"Compares average {measure.name} across {dim.name}, "
                    "useful for per-unit performance rather than raw volume."
                ),
                options={"dimension_cardinality": dim.cardinality},
            ))
    return specs


def _measure_over_time_lines(measures, datetimes) -> List[ChartSpec]:
    specs = []
    for dt in datetimes:
        for measure in measures:
            specs.append(ChartSpec(
                name=f"{measure.name}_over_{dt.name}",
                chart_type=ChartType.LINE,
                x=Axis(column=dt.name, label=_label(dt.name)),
                y=Axis(column=measure.name, label=_label(measure.name), unit=measure.unit),
                aggregation=Aggregation.SUM,
                reason=(
                    f"Tracks {measure.name} trend over {dt.name}, useful for "
                    "spotting growth, seasonality, or drop-offs."
                ),
            ))
    return specs


def _dimension_distributions(dimensions) -> List[ChartSpec]:
    specs = []
    for dim in dimensions:
        specs.append(ChartSpec(
            name=f"{dim.name}_distribution",
            chart_type=ChartType.PIE,
            x=Axis(column=dim.name, label=_label(dim.name)),
            reason=f"Shows the share of records across each {dim.name} category.",
            options={"dimension_cardinality": dim.cardinality},
        ))
    return specs


def _measure_distributions(measures) -> List[ChartSpec]:
    specs = []
    for measure in measures:
        specs.append(ChartSpec(
            name=f"{measure.name}_histogram",
            chart_type=ChartType.HISTOGRAM,
            x=Axis(column=measure.name, label=_label(measure.name), unit=measure.unit),
            reason=f"Shows how {measure.name} values are distributed — spots skew and typical range.",
        ))
        specs.append(ChartSpec(
            name=f"{measure.name}_boxplot",
            chart_type=ChartType.BOXPLOT,
            x=Axis(column=measure.name, label=_label(measure.name), unit=measure.unit),
            reason=f"Highlights the median, spread, and outliers in {measure.name}.",
        ))
    return specs


def _correlation_scatters(correlations, measures) -> List[ChartSpec]:
    measure_names = {m.name for m in measures}
    specs = []
    for corr in correlations:
        col_a, col_b = corr.get("columnA"), corr.get("columnB")
        value = corr.get("value")
        if col_a not in measure_names or col_b not in measure_names:
            continue
        if value is None or pd.isna(value):
            continue
        if abs(value) < MIN_CORRELATION_FOR_SCATTER:
            continue
        strength = "strong" if abs(value) > 0.6 else "moderate"
        direction = "positive" if value > 0 else "negative"
        specs.append(ChartSpec(
            name=f"{col_a}_vs_{col_b}",
            chart_type=ChartType.SCATTER,
            x=Axis(column=col_a, label=_label(col_a)),
            y=Axis(column=col_b, label=_label(col_b)),
            reason=(
                f"{col_a} and {col_b} show a {strength} {direction} "
                f"correlation ({value:.2f}), worth visualizing directly."
            ),
            options={"correlation": value},
        ))
    return specs


def _correlation_heatmap(measures) -> List[ChartSpec]:
    if len(measures) < 3:
        return []
    return [ChartSpec(
        name="correlation_heatmap",
        chart_type=ChartType.HEATMAP,
        reason="Overview of how all numeric fields relate to each other at once.",
    )]