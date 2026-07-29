from pydantic import BaseModel
from typing import Any

class InsightsRequest(BaseModel):
    session_id: str
    dataset_name: str
    profile: dict[str, Any]
    charts: list[dict[str, Any]]