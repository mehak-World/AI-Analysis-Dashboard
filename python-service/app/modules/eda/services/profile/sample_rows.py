import pandas as pd

def get_sample_rows(df: pd.DataFrame, limit: int = 5) -> list[dict]:
    sample_df = df.head(limit).astype(object)

    sample_df = sample_df.where(pd.notnull(sample_df), None)

    return sample_df.to_dict(orient="records")