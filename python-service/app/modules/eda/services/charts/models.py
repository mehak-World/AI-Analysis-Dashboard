"""
Internal models used by the chart generation pipeline.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ChartType(str, Enum):
    BAR = "bar"
    LINE = "line"
    SCATTER = "scatter"
    PIE = "pie"
    HISTOGRAM = "histogram"
    HEATMAP = "heatmap"
    BOXPLOT = "boxplot"


class Aggregation(str, Enum):
    SUM = "sum"
    MEAN = "mean"
    MEDIAN = "median"
    COUNT = "count"
    MIN = "min"
    MAX = "max"
    NONE = "none"


class SortOrder(str, Enum):
    NONE = "none"
    ASC = "asc"
    DESC = "desc"


@dataclass
class Axis:
    column: str
    label: str
    unit: str = ""


@dataclass
class ChartSpec:
    """
    Internal chart specification.

    Produced by recommender.py.
    Consumed by generator.py.
    """
    name: str
    chart_type: ChartType
    x: Optional[Axis] = None
    y: Optional[Axis] = None
    aggregation: Aggregation = Aggregation.NONE
    sort: SortOrder = SortOrder.NONE
    limit: Optional[int] = None
    reason: str = ""
    priority: int = 0
    options: dict = field(default_factory=dict)