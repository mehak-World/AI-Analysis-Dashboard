"""
DataFrame normalization utilities.

Responsible for normalizing raw dataset values
before profiling and analysis.
"""

import pandas as pd


DATETIME_COLUMN_NAMES = {
    "created_at",
    "updated_at",
    "createdAt",
    "updatedAt",
    "date",
    "datetime",
    "timestamp",
}


def normalize_datetime_columns(
    df: pd.DataFrame,
) -> pd.DataFrame:

    df = df.copy()

    for column in df.columns:

        column_name = column.strip().lower()

        if column_name not in DATETIME_COLUMN_NAMES:
            continue

        converted = pd.to_datetime(
            df[column],
            errors="coerce",
        )

        # Only convert when most values were
        # successfully interpreted as dates.
        if converted.notna().mean() >= 0.5:
            df[column] = converted

    return df