"""
Builds structured evidence from distribution statistics.

This evidence is later given to Gemini to explain.
"""

def build_distribution_evidence(
    distribution_plan,
    statistics,
):

    if distribution_plan.analysis_type == "numeric_distribution":
        return _numeric_evidence(statistics)

    if distribution_plan.analysis_type == "categorical_distribution":
        return _categorical_evidence(statistics)

    raise ValueError(
        f"Unsupported analysis type '{distribution_plan.analysis_type}'."
    )


# --------------------------------------------------
# Numeric
# --------------------------------------------------

def _numeric_evidence(stats):

    skewness = stats["skewness"]

    if skewness > 1:
        shape = "strongly right-skewed"
    elif skewness > 0.5:
        shape = "moderately right-skewed"
    elif skewness < -1:
        shape = "strongly left-skewed"
    elif skewness < -0.5:
        shape = "moderately left-skewed"
    else:
        shape = "approximately symmetric"

    outlier_pct = round(
        (stats["outlier_count"] / stats["count"] * 100)
        if stats["count"] else 0,
        2,
    )

    return {
        "shape": shape,
        "skewness": skewness,
        "mean": stats["mean"],
        "median": stats["median"],
        "std": stats["std"],
        "outlier_count": stats["outlier_count"],
        "outlier_percentage": outlier_pct,
        "range": {
            "min": stats["min"],
            "max": stats["max"],
        },
    }


# --------------------------------------------------
# Categorical / Boolean
# --------------------------------------------------

def _categorical_evidence(stats):

    value_counts = stats["value_counts"]

    if not value_counts:
        return {
            "dominant_category": None,
            "concentration": 0,
            "unique_count": stats["unique_count"],
        }

    top = value_counts[0]

    return {
        "dominant_category": top["value"],
        "dominant_percentage": top["percentage"],
        "concentration":
            "highly concentrated"
            if top["percentage"] >= 50
            else "moderately concentrated"
            if top["percentage"] >= 25
            else "evenly spread",
        "unique_count": stats["unique_count"],
    }