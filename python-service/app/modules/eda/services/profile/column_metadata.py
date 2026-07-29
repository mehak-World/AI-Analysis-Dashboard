import pandas as pd

def detect_category(series: pd.Series) -> str:
    """
    Detect the high-level category of a pandas Series.
    """

    if pd.api.types.is_bool_dtype(series):
        return "boolean"

    if pd.api.types.is_numeric_dtype(series):
        return "numeric"

    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"

    return "categorical"


def get_column_metadata(df: pd.DataFrame) -> list[dict]:
    """
    Generate metadata for every column in the dataset.
    """

    metadata = []

    for column in df.columns:
        non_null = df[column].dropna()

        metadata.append(
            {
                "name": column,

                "dtype": str(df[column].dtype),

                "category": detect_category(df[column]),

                # Will be populated later by Gemini
                "description": "",

                # Will be populated later by Gemini
                "unit": "",

                "exampleValues": [
                    str(value)
                    for value in non_null.astype(str).unique()[:5]
                ],
            }
        )

    return metadata