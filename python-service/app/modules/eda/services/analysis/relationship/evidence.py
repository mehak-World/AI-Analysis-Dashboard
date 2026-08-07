"""
Builds structured evidence from relationship statistics.

This evidence is later given to Gemini to explain.
"""

def build_relationship_evidence(
    relationship_plan,
    statistics,
):

    if relationship_plan.analysis_type == "correlation":
        return _correlation_evidence(statistics)

    if relationship_plan.analysis_type == "group_comparison":
        return _group_comparison_evidence(statistics)

    if relationship_plan.analysis_type == "association":
        return _association_evidence(statistics)

    if relationship_plan.analysis_type == "trend":
        return _trend_evidence(statistics)

    raise ValueError(
        f"Unsupported analysis type '{relationship_plan.analysis_type}'."
    )


# --------------------------------------------------
# Numeric ↔ Numeric
# --------------------------------------------------

def _correlation_evidence(stats):

    pearson = stats.get("pearson")

    strength = "weak"

    if abs(pearson) >= 0.8:
        strength = "very strong"

    elif abs(pearson) >= 0.6:
        strength = "strong"

    elif abs(pearson) >= 0.4:
        strength = "moderate"

    elif abs(pearson) >= 0.2:
        strength = "weak"

    direction = (
        "positive"
        if pearson >= 0
        else "negative"
    )

    return {
        "relationship": True,
        "strength": strength,
        "direction": direction,
        "pearson": pearson,
        "sample_size": stats["count"],
    }


# --------------------------------------------------
# Numeric ↔ Category
# --------------------------------------------------

def _group_comparison_evidence(stats):

    groups = stats["groups"]

    highest = max(
        groups,
        key=lambda x: x["mean"],
    )

    lowest = min(
        groups,
        key=lambda x: x["mean"],
    )

    return {
        "highest_group": highest,
        "lowest_group": lowest,
        "difference":
            highest["mean"] - lowest["mean"],
    }


# --------------------------------------------------
# Category ↔ Category
# --------------------------------------------------

def _association_evidence(stats):

    return {
        "chi_square": stats["chi_square"],
        "p_value": stats["p_value"],
        "association":
            stats["p_value"] < 0.05,
    }


# --------------------------------------------------
# Trend
# --------------------------------------------------

def _trend_evidence(stats):

    trend = stats["trend"]

    if len(trend) < 2:

        return {
            "trend": "unknown"
        }

    first = trend[0]
    last = trend[-1]

    return {
        "trend":
            "increasing"
            if last != first
            else "stable"
    }