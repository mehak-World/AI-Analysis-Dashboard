"""
Models for trend analysis.
"""

from typing import List

from pydantic import BaseModel
class TrendPlan(BaseModel):
    x: str
    y: str
    analysis_type: str
    time_column: str
    metric: str
    aggregation: str
    statistics: list[str]
    chart_type: str

    frequency: str = "day"
    