from dataclasses import dataclass, field


@dataclass
class CompositionPlan:
    category: str
    subcategory: str | None
    value: str | None
    analysis_type: str
    chart_type: str
    max_slices: int
    statistics: list[str] = field(default_factory=list)
    use_ai_explanation: bool = True