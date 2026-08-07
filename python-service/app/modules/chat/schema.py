from pydantic import BaseModel

class PlannerRequest(BaseModel):
    question: str
    s3_key: str
    dataset_name: str
    dataset_profile: dict
    column_metadata: list
    dataset_summary: dict
    correlations: list
    existing_charts: list