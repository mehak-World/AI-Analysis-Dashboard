"""
Builds structured evidence from composition statistics.

This evidence is later given to Gemini to explain.
"""

def build_composition_evidence(
    composition_plan,
    statistics,
):

    if composition_plan.analysis_type == "composition_hierarchical":
        return _hierarchical_evidence(statistics)

    return _flat_evidence(statistics)


# --------------------------------------------------
# Flat (by_count / by_value)
# --------------------------------------------------

def _flat_evidence(stats):

    parts = stats["parts"]

    if not parts:
        return {
            "largest_part": None,
            "smallest_part": None,
            "concentration": None,
        }

    largest = parts[0]
    smallest = parts[-1]

    top_share = round(
        sum(p["share_of_total"] for p in parts[:3]),
        2,
    )

    return {
        "metric": stats["value_column"],
        "largest_part": largest,
        "smallest_part": smallest,
        "top_3_share_of_total": top_share,
        "concentration":
            "dominated by a few parts"
            if top_share >= 60
            else "moderately concentrated"
            if top_share >= 35
            else "evenly split",
        "total_parts": len(parts),
        "unique_categories": stats["unique_categories"],
    }


# --------------------------------------------------
# Hierarchical
# --------------------------------------------------

def _hierarchical_evidence(stats):

    parts = stats["parts"]

    if not parts:
        return {
            "largest_category": None,
            "largest_subcategory": None,
        }

    largest_category = parts[0]

    largest_subcategory = None

    if largest_category["children"]:
        largest_subcategory = largest_category["children"][0]

    return {
        "largest_category": {
            "category": largest_category["category"],
            "value": largest_category["value"],
        },
        "largest_subcategory_within_it": largest_subcategory,
        "total_categories": len(parts),
        "total_subcategories": stats["unique_subcategories"],
    }