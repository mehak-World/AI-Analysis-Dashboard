import pandas as pd


def get_correlations(
    df: pd.DataFrame,
    min_correlation: float = 0.3,
) -> list[dict]:
    """
    Computes pairwise correlations between numeric columns.

    Returns only correlations whose absolute value is greater than
    or equal to min_correlation.
    """

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.shape[1] < 2:
        return []

    # Remove constant columns
    numeric_df = numeric_df.loc[:, numeric_df.nunique() > 1]

    if numeric_df.shape[1] < 2:
        return []

    corr_matrix = numeric_df.corr()
    correlations = []
    columns = corr_matrix.columns.tolist()

    for i in range(len(columns)):
        for j in range(i + 1, len(columns)):
            value = corr_matrix.iloc[i, j]

            if pd.isna(value):
                continue

            if abs(value) < min_correlation:
                continue

            correlations.append(
                {
                    "columnA": columns[i],
                    "columnB": columns[j],
                    "value": round(float(value), 4),

                    # Gemini will fill this later
                    "explanation": "",
                }
            )

    correlations.sort(
        key=lambda x: abs(x["value"]),
        reverse=True,
    )

    return correlations