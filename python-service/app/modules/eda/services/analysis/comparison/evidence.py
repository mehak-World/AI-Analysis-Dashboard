"""
Builds structured evidence from comparison statistics.

This evidence is later given to Gemini to explain
the comparison results.

No AI is used here.
"""


def build_comparison_evidence(
    comparison_plan,
    statistics,
):

    if comparison_plan.comparison_type == "numeric_by_category":
        return _numeric_by_category_evidence(
            comparison_plan,
            statistics,
        )

    if comparison_plan.comparison_type == "rate_by_category":
        return _rate_by_category_evidence(
            comparison_plan,
            statistics,
        )

    raise ValueError(
        f"Unsupported comparison type "
        f"'{comparison_plan.comparison_type}'."
    )


# --------------------------------------------------
# Numeric by Category
# --------------------------------------------------

def _numeric_by_category_evidence(
    plan,
    stats,
):

    groups = stats.get("groups", [])

    if not groups:
        return {
            "comparison": False,
            "reason": "No valid groups found.",
        }

    highest = stats.get("highest_group")
    lowest = stats.get("lowest_group")
    difference = stats.get("difference")

    return {
        "comparison": True,

        "comparison_type": "numeric_by_category",

        "metric": plan.metric,
        "group": plan.group,

        "highest_group": highest,
        "lowest_group": lowest,

        "difference": difference,

        "groups": groups,

        "sample_size": stats.get(
            "sample_size"
        ),
    }


# --------------------------------------------------
# Rate by Category
# --------------------------------------------------

def _rate_by_category_evidence(
    plan,
    stats,
):

    groups = stats.get("groups", [])

    if not groups:
        return {
            "comparison": False,
            "reason": "No valid groups found.",
        }

    highest = stats.get("highest_group")
    lowest = stats.get("lowest_group")
    difference = stats.get("difference")

    # Convert rate difference to percentage points.
    difference_percentage_points = (
        round(difference * 100, 2)
        if difference is not None
        else None
    )

    # Add percentage representation to each group.
    enriched_groups = []

    for group in groups:

        enriched_group = {
            **group,
            "rate_percentage": round(
                group["rate"] * 100,
                2,
            ),
        }

        enriched_groups.append(
            enriched_group
        )

    enriched_highest = None

    if highest:
        enriched_highest = {
            **highest,
            "rate_percentage": round(
                highest["rate"] * 100,
                2,
            ),
        }

    enriched_lowest = None

    if lowest:
        enriched_lowest = {
            **lowest,
            "rate_percentage": round(
                lowest["rate"] * 100,
                2,
            ),
        }

    return {
        "comparison": True,

        "comparison_type": "rate_by_category",

        "group": plan.group,
        "outcome": plan.outcome,

        "positive_value": stats.get(
            "positive_value"
        ),

        "highest_group": enriched_highest,
        "lowest_group": enriched_lowest,

        "difference": difference,

        "difference_percentage_points":
            difference_percentage_points,

        "groups": enriched_groups,

        "sample_size": stats.get(
            "sample_size"
        ),
    }