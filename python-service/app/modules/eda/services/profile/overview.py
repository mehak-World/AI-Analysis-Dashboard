import pandas as pd


def get_overview(df: pd.DataFrame) -> dict:
    total_rows = len(df)

    return {
        "rowCount": total_rows,
        "columnCount": len(df.columns),
        "columns": df.columns.tolist(),

        "dtypes": {
            column: str(dtype)
            for column, dtype in df.dtypes.items()
        },

        "nullCounts": {
            column: int(count)
            for column, count in df.isnull().sum().items()
        },

        "nullPercents": {
            column: round((count / total_rows) * 100, 2)
            if total_rows > 0 else 0
            for column, count in df.isnull().sum().items()
        },

        "duplicateRows": int(df.duplicated().sum())
    }