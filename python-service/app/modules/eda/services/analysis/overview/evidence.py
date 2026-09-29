"""
Builds structured evidence from overview statistics.

This evidence is later given to Gemini to explain.
"""

def build_overview_evidence(overview_plan, statistics):

    profile = statistics["profile"]

    evidence = {
        "shape": {
            "rows": profile["rows"],
            "columns": profile["columns"],
        },
        "duplicate_rows": profile["duplicate_rows"],
        "column_types": {
            "numeric": len(profile["numeric_columns"]),
            "categorical": len(profile["categorical_columns"]),
        },
    }

    if "missing_values" in statistics:
        missing = statistics["missing_values"]

        evidence["missing_values"] = {
            "total_missing_cells": missing["total_missing_cells"],
            "worst_columns": missing["columns_with_missing"][:5],
        }

    if "correlations" in statistics:
        evidence["strongest_correlations"] = statistics["correlations"]["top_pairs"][:5]

    return evidence