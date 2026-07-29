import pandas as pd
import numpy as np


def get_numeric_summary(df: pd.DataFrame) -> dict:
    numeric_df = df.select_dtypes(include=np.number)

    if numeric_df.empty:
        return {}

    summary = numeric_df.describe().T.round(4)

    result = {}

    for column, values in summary.iterrows():
        result[column] = {
            key: float(value) if pd.notna(value) else None
            for key, value in values.items()
        }

    return result