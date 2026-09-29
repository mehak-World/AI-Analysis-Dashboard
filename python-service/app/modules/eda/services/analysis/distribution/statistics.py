"""
Distribution statistics engine.

Computes the statistical evidence required for
a DistributionPlan.
"""

import pandas as pd
import numpy as np

from scipy.stats import skew, kurtosis


def generate_distribution_statistics(
    df: pd.DataFrame,
    plan,
) -> dict:

    if plan.analysis_type == "numeric_distribution":
        return _numeric_distribution(df, plan)

    if plan.analysis_type == "categorical_distribution":
        return _categorical_distribution(df, plan)

    raise ValueError(
        f"Unsupported analysis '{plan.analysis_type}'."
    )


# ---------------------------------------------------
# Numeric
# ---------------------------------------------------
def _numeric_distribution(
    df,
    plan,
):

    series = df[plan.column].dropna()

    if len(series) < 3:
        return {
            "count": int(series.count()),
            "missing": int(df[plan.column].isna().sum()),
            "insufficient_data": True,
        }

    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = series[
        (series < lower_bound)
        | (series > upper_bound)
    ]

    percentiles = {
        "p5": series.quantile(0.05),
        "p25": q1,
        "p50": series.quantile(0.50),
        "p75": q3,
        "p90": series.quantile(0.90),
        "p95": series.quantile(0.95),
        "p99": series.quantile(0.99),
    }

    percentiles = {
        k: round(float(v), 4)
        for k, v in percentiles.items()
    }

    return {
        "count": int(series.count()),
        "missing": int(df[plan.column].isna().sum()),
        "mean": round(float(series.mean()), 4),
        "median": round(float(series.median()), 4),
        "std": round(float(series.std()), 4),
        "min": round(float(series.min()), 4),
        "max": round(float(series.max()), 4),
        "skewness": round(float(skew(series)), 4),
        "kurtosis": round(float(kurtosis(series)), 4),
        "percentiles": percentiles,
        "outlier_count": int(len(outliers)),
        "outlier_bounds": {
            "lower": round(float(lower_bound), 4),
            "upper": round(float(upper_bound), 4),
        },
        "insufficient_data": False,
    }

# ---------------------------------------------------
# Categorical / Boolean
# ---------------------------------------------------

def _categorical_distribution(
    df,
    plan,
):

    series = df[plan.column]

    value_counts = (
        series.value_counts()
        .head(15)
    )

    total = len(series)

    value_counts_list = [
        {
            "value": str(index),
            "count": int(count),
            "percentage": round(float(count / total * 100), 2),
        }
        for index, count in value_counts.items()
    ]

    mode = series.mode()

    return {
        "count": int(total),
        "missing": int(series.isna().sum()),
        "unique_count": int(series.nunique()),
        "mode": str(mode.iloc[0]) if not mode.empty else None,
        "value_counts": value_counts_list,
    }