from dataclasses import dataclass, field


@dataclass
class DistributionPlan:
    column: str
    analysis_type: str
    chart_type: str
    statistics: list[str] = field(default_factory=list)
    use_ai_explanation: bool = True