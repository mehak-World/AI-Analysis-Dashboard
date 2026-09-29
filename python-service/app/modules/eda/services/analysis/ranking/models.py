from dataclasses import dataclass, field


@dataclass
class RankingPlan:
    category: str
    value: str | None
    analysis_type: str
    chart_type: str
    aggregation: str
    order: str
    top_n: int
    statistics: list[str] = field(default_factory=list)
    use_ai_explanation: bool = True