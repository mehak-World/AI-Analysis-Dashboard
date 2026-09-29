from pydantic import BaseModel
from typing import List


class ComparisonPlan(BaseModel):
    x: str
    y: str

    comparison_type: str

    metric: str | None = None
    group: str | None = None
    outcome: str | None = None

    statistics: List[str]
    chart_type: str