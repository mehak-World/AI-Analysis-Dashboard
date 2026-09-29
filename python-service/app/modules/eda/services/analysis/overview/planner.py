"""
Overview analysis planner.

Determines which dataset-level analyses are applicable
based on the shape and dtypes of the dataframe.

No AI is used here.
"""

from pandas.api.types import is_numeric_dtype, is_bool_dtype

from .models import OverviewPlan


def build_overview_plan(df) -> OverviewPlan:

    numeric_columns = [
        col for col in df.columns
        if is_numeric_dtype(df[col]) and not is_bool_dtype(df[col])
    ]

    return OverviewPlan(
        include_correlations=len(numeric_columns) >= 2,
        include_missing_values=True,
        include_summary=True,
    )