from .column_metadata import get_column_metadata
from .dataset_profile import get_dataset_summary
from .numeric_summary import get_numeric_summary
from .overview import get_overview
from .sample_rows import get_sample_rows
from .correlations import get_correlations

import json

async def run_profile(df):
    overview = get_overview(df)
    numeric_summary = get_numeric_summary(df)
    dataset_profile = get_dataset_summary(df)
    sample_rows = get_sample_rows(df)
    column_metadata = get_column_metadata(df)
    correlations = get_correlations(df)


    response = {
        **overview,
        "numericSummary": numeric_summary,
        "datasetProfile": dataset_profile,
        "sampleRows": sample_rows,
        "columnMetadata": column_metadata,
        "correlations": correlations,
    }

    for name, value in response.items():
        try:
            json.dumps(value, allow_nan=False)
            print(f"✅ {name} OK")
        except ValueError as e:
            print(f"❌ {name} FAILED")
            raise

    return response