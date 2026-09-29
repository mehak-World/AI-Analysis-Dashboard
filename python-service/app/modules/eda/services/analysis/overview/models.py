from dataclasses import dataclass


@dataclass
class OverviewPlan:
    include_correlations: bool
    include_missing_values: bool
    include_summary: bool
    analysis_type: str = "dataset_overview"
    use_ai_explanation: bool = True