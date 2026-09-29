"""
Overview statistics engine.

Computes dataset-level profile, missing values,
correlations, and summary statistics.
"""

import pandas as pd
from pandas.api.types import is_numeric_dtype, is_bool_dtype


def generate_overview_statistics(df: pd.DataFrame, plan) -> dict:

    result = {
        "profile": _profile(df),
    }

    if plan.include_missing_values:
        result["missing_values"] = _missing_values(df)

    if plan.include_correlations:
        result["correlations"] = _correlations(df)

    if plan.include_summary:
        result["summary"] = _summary(df)

    return result


# ---------------------------------------------------
# Profile
# ---------------------------------------------------

def _profile(df):

    numeric_cols = [
        col for col in df.columns
        if is_numeric_dtype(df[col]) and not is_bool_dtype(df[col])
    ]

    categorical_cols = [
        col for col in df.columns
        if col not in numeric_cols
    ]

    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "numeric_columns": numeric_cols,
        "categorical_columns": categorical_cols,
        "duplicate_rows": int(df.duplicated().sum()),
    }


# ---------------------------------------------------
# Missing values
# ---------------------------------------------------

def _missing_values(df):

    total_rows = len(df)

    missing = df.isna().sum()

    rows = [
        {
            "column": col,
            "missing_count": int(count),
            "missing_percentage": round(float(count / total_rows * 100), 2) if total_rows else 0,
        }
        for col, count in missing.items()
        if count > 0
    ]

    rows.sort(key=lambda r: r["missing_count"], reverse=True)

    return {
        "columns_with_missing": rows,
        "total_missing_cells": int(missing.sum()),
    }


# ---------------------------------------------------
# Correlations
# ---------------------------------------------------

def _correlations(df):

    numeric_cols = [
        col for col in df.columns
        if is_numeric_dtype(df[col]) and not is_bool_dtype(df[col])
    ]

    corr_matrix = df[numeric_cols].corr(method="pearson").round(4)

    pairs = []

    for i, col_a in enumerate(numeric_cols):
        for col_b in numeric_cols[i + 1:]:
            value = corr_matrix.loc[col_a, col_b]

            if pd.isna(value):
                continue

            pairs.append({
                "column_a": col_a,
                "column_b": col_b,
                "correlation": float(value),
            })

    pairs.sort(key=lambda p: abs(p["correlation"]), reverse=True)

    return {
        "top_pairs": pairs[:10],
    }


# ---------------------------------------------------
# Summary
# ---------------------------------------------------

def _summary(df):

    numeric_cols = [
        col for col in df.columns
        if is_numeric_dtype(df[col]) and not is_bool_dtype(df[col])
    ]

    categorical_cols = [
        col for col in df.columns
        if col not in numeric_cols
    ]

    numeric_summary = {}

    for col in numeric_cols:
        series = df[col].dropna()

        if series.empty:
            continue

        numeric_summary[col] = {
            "mean": round(float(series.mean()), 4),
            "median": round(float(series.median()), 4),
            "std": round(float(series.std()), 4),
            "min": round(float(series.min()), 4),
            "max": round(float(series.max()), 4),
        }

    categorical_summary = {}

    for col in categorical_cols:
        series = df[col].dropna()

        if series.empty:
            continue

        mode = series.mode()

        categorical_summary[col] = {
            "unique_count": int(series.nunique()),
            "mode": str(mode.iloc[0]) if not mode.empty else None,
        }

    return {
        "numeric": numeric_summary,
        "categorical": categorical_summary,
    }