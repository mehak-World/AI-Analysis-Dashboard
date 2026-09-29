"""
Builds structured evidence from ranking statistics.

This evidence is later given to Gemini to explain.
"""

def build_ranking_evidence(
    ranking_plan,
    statistics,
):

    ranked = statistics["ranked"]

    if not ranked:
        return {
            "leader": None,
            "gap_to_second": None,
            "concentration": None,
        }

    leader = ranked[0]

    gap_to_second = None

    if len(ranked) > 1:
        second = ranked[1]
        gap_to_second = round(
            leader["value"] - second["value"],
            4,
        )

    top_3_share = round(
        sum(
            row["share_of_total"]
            for row in ranked[:3]
        ),
        2,
    )

    return {
        "metric": statistics["value_column"],
        "leader": leader,
        "gap_to_second": gap_to_second,
        "top_3_share_of_total": top_3_share,
        "concentration":
            "highly concentrated at the top"
            if top_3_share >= 60
            else "moderately concentrated"
            if top_3_share >= 35
            else "evenly distributed",
        "total_ranked": len(ranked),
        "unique_categories": statistics["unique_categories"],
    }