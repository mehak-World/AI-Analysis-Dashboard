"""
Chart generation orchestrator (updated).

Runs chart recommendation and Gemini follow-up-question suggestions
concurrently since neither depends on the other's output, then
generates the actual chart data/statistics from the selected specs.
"""
import asyncio

from app.modules.eda.services.charts.recommender import (
    recommend_charts,
    suggest_followup_questions,
)
from app.modules.eda.services.charts.generator import generate_charts
from app.modules.eda.services.charts.classifier import classify_dataset
from app.modules.eda.services.charts.json_safety import sanitize_for_json

from app.modules.eda.services.profile.column_metadata import get_column_metadata
from app.modules.eda.services.profile.correlations import get_correlations


async def run_charts(df):
    column_metadata = get_column_metadata(df)
    correlations = get_correlations(df)
    dataset_type = classify_dataset(column_metadata)

    chart_specs, suggested_questions = await asyncio.gather(
        recommend_charts(
            df=df,
            column_metadata=column_metadata,
            correlations=correlations,
        ),
        suggest_followup_questions(
            column_metadata=column_metadata,
            dataset_type=dataset_type.value,
        ),
    )

    charts = generate_charts(
        df=df,
        chart_specs=chart_specs,
    )

    return sanitize_for_json({
        "charts": charts,
        "suggestedQuestions": suggested_questions,
    })