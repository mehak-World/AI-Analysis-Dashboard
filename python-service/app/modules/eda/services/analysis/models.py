from dataclasses import dataclass, field

from .intents import Intent

@dataclass
class IntentDefinition:
    analyses: list[str] = field(default_factory=list)
    preferred_visualizations: list[str] = field(default_factory=list)
    use_ai_explanation: bool = True


@dataclass
class AnalysisPlan:
    intent: Intent
    user_question: str
    analysis_goal: str = ""
    entities: list[str] = field(default_factory=list)
    filters: dict = field(default_factory=dict)
    chart_id: str | None = None
    existing_chart: bool = False
    requested_chart: bool = False
    requested_prediction: bool = False
    requested_explanation: bool = True
    requested_recommendation: bool = False
    preferred_chart: str | None = None
    confidence: float = 1.0

@dataclass
class ExecutionResult:
    plan: AnalysisPlan
    charts: list = field(default_factory=list)
    statistics: dict = field(default_factory=dict)
    evidence: dict = field(default_factory=dict)
    explanation: str = ""
    recommendations: list[str] = field(default_factory=list)
    prediction: dict | None = None