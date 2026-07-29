import pandas as pd
import numpy as np


def get_dataset_summary(df: pd.DataFrame) -> dict:
    numeric_columns = df.select_dtypes(include=np.number).columns
    categorical_columns = df.select_dtypes(include=["object", "category"]).columns
    datetime_columns = df.select_dtypes(include=["datetime64"]).columns
    boolean_columns = df.select_dtypes(include="bool").columns

    total_missing = int(df.isnull().sum().sum())

    return {
        "datasetSizeMB": round(
            df.memory_usage(deep=True).sum() / (1024 * 1024),
            2,
        ),

        "numericColumns": len(numeric_columns),

        "categoricalColumns": len(categorical_columns),

        "datetimeColumns": len(datetime_columns),

        "booleanColumns": len(boolean_columns),

        "duplicateRows": int(df.duplicated().sum()),

        "missingValues": total_missing,
    }