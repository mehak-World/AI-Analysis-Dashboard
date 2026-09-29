"""
Builds structured evidence for trend analysis.

The evidence layer interprets the deterministic statistics.
It does NOT call AI and does NOT invent explanations.
"""

import numpy as np
import pandas as pd


def build_trend_evidence(
    trend_plan,
    statistics,
):

    if trend_plan.analysis_type == "time_series":
        return _time_series_evidence(
            trend_plan,
            statistics,
        )

    if trend_plan.analysis_type == "growth_rate":
        return _growth_rate_evidence(
            trend_plan,
            statistics,
        )

    if trend_plan.analysis_type == "moving_average":
        return _moving_average_evidence(
            trend_plan,
            statistics,
        )

    raise ValueError(
        f"Unsupported trend analysis "
        f"'{trend_plan.analysis_type}'."
    )


# --------------------------------------------------
# Time Series
# --------------------------------------------------

def _time_series_evidence(
    plan,
    stats,
):

    points = stats.get(
        "points",
        [],
    )

    if not points:

        return {
            "trend": False,
            "trend_type": "time_series",
            "time_column": plan.time_column,
            "metric": plan.metric,
            "aggregation": plan.aggregation,
            "frequency": plan.frequency,
            "direction": "unknown",
            "trend_strength": "unknown",
            "sample_size": stats.get(
                "sample_size",
                0,
            ),
            "points": [],
        }

    # --------------------------------------------------
    # Extract values
    # --------------------------------------------------

    values = [
        float(point["value"])
        for point in points
        if point.get("value") is not None
    ]

    if not values:

        return {
            "trend": False,
            "trend_type": "time_series",
            "time_column": plan.time_column,
            "metric": plan.metric,
            "aggregation": plan.aggregation,
            "frequency": plan.frequency,
            "direction": "unknown",
            "trend_strength": "unknown",
            "sample_size": stats.get(
                "sample_size",
                0,
            ),
            "points": points,
        }

    # --------------------------------------------------
    # Basic statistics
    # --------------------------------------------------

    first_value = values[0]
    last_value = values[-1]

    minimum = min(values)
    maximum = max(values)

    min_index = values.index(
        minimum
    )

    max_index = values.index(
        maximum
    )

    min_point = points[min_index]
    max_point = points[max_index]

    change = (
        last_value -
        first_value
    )

    if first_value != 0:

        percentage_change = (
            change /
            abs(first_value)
        ) * 100

    else:

        percentage_change = None

    # --------------------------------------------------
    # Linear trend
    # --------------------------------------------------

    direction = "stable"
    trend_strength = "weak"

    if len(values) >= 2:

        x = np.arange(
            len(values),
            dtype=float,
        )

        y = np.array(
            values,
            dtype=float,
        )

        slope = np.polyfit(
            x,
            y,
            1,
        )[0]

        correlation = np.corrcoef(
            x,
            y,
        )[0, 1]

        if np.isnan(correlation):
            correlation = 0.0

        abs_correlation = abs(
            correlation
        )

        # ----------------------------------------------
        # Direction
        # ----------------------------------------------

        if abs_correlation < 0.2:

            direction = "stable"

        elif slope > 0:

            direction = "increasing"

        else:

            direction = "decreasing"

        # ----------------------------------------------
        # Strength
        # ----------------------------------------------

        if abs_correlation >= 0.8:

            trend_strength = "strong"

        elif abs_correlation >= 0.5:

            trend_strength = "moderate"

        else:

            trend_strength = "weak"

    else:

        slope = None
        correlation = None

    # --------------------------------------------------
    # Volatility
    # --------------------------------------------------

    if len(values) >= 2:

        mean_value = np.mean(
            values
        )

        std_value = np.std(
            values
        )

        if mean_value != 0:

            coefficient_variation = (
                std_value /
                abs(mean_value)
            )

        else:

            coefficient_variation = 0

        if coefficient_variation >= 1:

            volatility = "high"

        elif coefficient_variation >= 0.5:

            volatility = "moderate"

        else:

            volatility = "low"

    else:

        volatility = "unknown"
        coefficient_variation = None

    # --------------------------------------------------
    # Build evidence
    # --------------------------------------------------

    return {

        "trend": True,

        "trend_type": "time_series",

        "time_column": plan.time_column,

        "metric": plan.metric,

        "aggregation": plan.aggregation,

        "frequency": plan.frequency,

        # ----------------------------------------------
        # Direction
        # ----------------------------------------------

        "direction": direction,

        "trend_strength": trend_strength,

        # ----------------------------------------------
        # Volatility
        # ----------------------------------------------

        "volatility": volatility,

        "coefficient_variation": (
            round(
                float(
                    coefficient_variation
                ),
                4,
            )
            if coefficient_variation is not None
            else None
        ),

        # ----------------------------------------------
        # Start / End
        # ----------------------------------------------

        "first_value": first_value,

        "last_value": last_value,

        "change": round(
            float(change),
            4,
        ),

        "percentage_change": (
            round(
                float(
                    percentage_change
                ),
                4,
            )
            if percentage_change is not None
            else None
        ),

        # ----------------------------------------------
        # Extremes
        # ----------------------------------------------

        "minimum": {
            "value": minimum,
            "period": min_point.get(
                plan.time_column
            ),
        },

        "maximum": {
            "value": maximum,
            "period": max_point.get(
                plan.time_column
            ),
        },

        # ----------------------------------------------
        # Trend model
        # ----------------------------------------------

        "slope": (
            round(
                float(slope),
                6,
            )
            if slope is not None
            else None
        ),

        "correlation_with_time": (
            round(
                float(correlation),
                4,
            )
            if correlation is not None
            else None
        ),

        # ----------------------------------------------
        # Dataset
        # ----------------------------------------------

        "observed_periods": len(points),

        "sample_size": stats.get(
            "sample_size",
            0,
        ),

        # ----------------------------------------------
        # Raw deterministic points
        # ----------------------------------------------

        "points": points,
    }


# --------------------------------------------------
# Growth Rate
# --------------------------------------------------

def _growth_rate_evidence(
    plan,
    stats,
):

    points = stats.get(
        "points",
        [],
    )

    growth_values = [
        point["growth_rate"]
        for point in points
        if point.get("growth_rate") is not None
    ]

    if not growth_values:

        return {
            "trend": False,
            "trend_type": "growth_rate",
            "direction": "unknown",
            "points": points,
        }

    positive = sum(
        value > 0
        for value in growth_values
    )

    negative = sum(
        value < 0
        for value in growth_values
    )

    if positive > negative:

        direction = "mostly_increasing"

    elif negative > positive:

        direction = "mostly_decreasing"

    else:

        direction = "mixed"

    return {

        "trend": True,

        "trend_type": "growth_rate",

        "time_column": plan.time_column,

        "metric": plan.metric,

        "direction": direction,

        "average_growth_rate": round(
            float(
                np.mean(
                    growth_values
                )
            ),
            4,
        ),

        "maximum_growth_rate": round(
            float(
                max(
                    growth_values
                )
            ),
            4,
        ),

        "minimum_growth_rate": round(
            float(
                min(
                    growth_values
                )
            ),
            4,
        ),

        "positive_periods": positive,

        "negative_periods": negative,

        "observed_periods": len(
            points
        ),

        "sample_size": stats.get(
            "sample_size",
            0,
        ),

        "points": points,
    }


# --------------------------------------------------
# Moving Average
# --------------------------------------------------

def _moving_average_evidence(
    plan,
    stats,
):

    points = stats.get(
        "points",
        [],
    )

    valid = [
        point
        for point in points
        if point.get(
            "moving_average"
        ) is not None
    ]

    if len(valid) < 2:

        return {
            "trend": False,
            "trend_type": "moving_average",
            "direction": "unknown",
            "window": stats.get(
                "window"
            ),
            "points": points,
        }

    first = valid[0][
        "moving_average"
    ]

    last = valid[-1][
        "moving_average"
    ]

    if last > first:

        direction = "increasing"

    elif last < first:

        direction = "decreasing"

    else:

        direction = "stable"

    return {

        "trend": True,

        "trend_type": "moving_average",

        "time_column": plan.time_column,

        "metric": plan.metric,

        "window": stats.get(
            "window"
        ),

        "direction": direction,

        "first_moving_average": first,

        "last_moving_average": last,

        "change": round(
            float(
                last - first
            ),
            4,
        ),

        "observed_periods": len(
            points
        ),

        "sample_size": stats.get(
            "sample_size",
            0,
        ),

        "points": points,
    }