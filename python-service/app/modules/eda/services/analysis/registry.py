from .intents import Intent
from .models import IntentDefinition
from .handlers import relationship
from .intents import Intent


INTENT_REGISTRY = {

    Intent.OVERVIEW: IntentDefinition(
        analyses=[
            "profile",
            "correlations",
            "missing_values",
            "summary",
        ],
        preferred_visualizations=[],
    ),

    Intent.RELATIONSHIP: IntentDefinition(
        analyses=[
            "correlation",
            "grouped_summary",
            "regression",
        ],
        preferred_visualizations=[
            "scatter",
            "grouped_bar",
        ],
    ),

    Intent.COMPARISON: IntentDefinition(
        analyses=[
            "group_comparison",
        ],
        preferred_visualizations=[
            "bar",
            "boxplot",
        ],
    ),

    Intent.TREND: IntentDefinition(
        analyses=[
            "time_series",
            "growth_rate",
            "moving_average",
        ],
        preferred_visualizations=[
            "line",
            "area",
        ],
    ),

    Intent.DISTRIBUTION: IntentDefinition(
        analyses=[
            "distribution",
            "outliers",
            "percentiles",
        ],
        preferred_visualizations=[
            "histogram",
            "boxplot",
        ],
    ),

    Intent.RANKING: IntentDefinition(
        analyses=[
            "ranking",
        ],
        preferred_visualizations=[
            "bar",
        ],
    ),

    Intent.COMPOSITION: IntentDefinition(
        analyses=[
            "composition",
        ],
        preferred_visualizations=[
            "pie",
            "treemap",
        ],
    ),

    Intent.DIAGNOSTIC: IntentDefinition(
        analyses=[
            "correlation",
            "feature_importance",
            "segments",
            "outliers",
            "distribution",
        ],
        preferred_visualizations=[
            "multiple",
        ],
    ),

    Intent.SEGMENTATION: IntentDefinition(
        analyses=[
            "segmentation",
        ],
        preferred_visualizations=[
            "cluster",
            "scatter",
        ],
    ),

    Intent.ANOMALY: IntentDefinition(
        analyses=[
            "outlier_detection",
        ],
        preferred_visualizations=[
            "scatter",
            "boxplot",
        ],
    ),

    Intent.PREDICTION: IntentDefinition(
        analyses=[
            "prediction",
        ],
        preferred_visualizations=[],
    ),

    Intent.WHAT_IF: IntentDefinition(
        analyses=[
            "prediction",
            "counterfactual",
        ],
        preferred_visualizations=[],
    ),

    Intent.RECOMMENDATION: IntentDefinition(
        analyses=[
            "prediction",
            "feature_importance",
            "counterfactual",
        ],
        preferred_visualizations=[],
    ),

    Intent.EXPLAIN: IntentDefinition(
        analyses=[],
        preferred_visualizations=[],
    ),
}


HANDLERS = {
    Intent.RELATIONSHIP: relationship.execute,

}