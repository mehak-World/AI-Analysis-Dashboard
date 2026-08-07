import json
import re

from app.core.gemini import ask_gemini
from app.modules.ai.prompts import build_planner_prompt

from .intents import Intent
from .models import AnalysisPlan

def extract_json(text: str):
    text = text.strip()

    # Remove markdown fences if Gemini returns them
    text = text.replace("```json", "")
    text = text.replace("```", "").strip()

    match = re.search(r"\{[\s\S]*\}", text)

    if not match:
        raise ValueError(f"No JSON found.\n\nGemini Response:\n{text}")

    return json.loads(match.group())

class AnalysisPlanner:

    async def plan(
        self,
        *,
        question: str,
        dataset_name: str,
        dataset_profile: dict,
        column_metadata: list[dict],
        dataset_summary: dict,
        correlations: list[dict],
        existing_charts: list[dict],
    ) -> AnalysisPlan:

        prompt = build_planner_prompt(
            question=question,
            dataset_name=dataset_name,
            dataset_profile=dataset_profile,
            column_metadata=column_metadata,
            dataset_summary=dataset_summary,
            correlations=correlations,
            existing_charts=existing_charts,
        )

        response = await ask_gemini(prompt)

        print("=" * 100)
        print(response)
        print("=" * 100)
        plan = extract_json(response)

        chart_id = plan.get("chart_id")

        return AnalysisPlan(
            intent=Intent(plan["intent"]),
            user_question=question,

            analysis_goal=plan.get(
                "analysis_goal",
                "",
            ),

            entities=plan.get(
                "entities",
                [],
            ),

            filters=plan.get(
                "filters",
                {},
            ),

            chart_id=chart_id,

            existing_chart=chart_id is not None,

            requested_chart=plan.get(
                "requested_chart",
                False,
            ),

            requested_prediction=plan.get(
                "requested_prediction",
                False,
            ),

            requested_explanation=plan.get(
                "requested_explanation",
                True,
            ),

            requested_recommendation=plan.get(
                "requested_recommendation",
                False,
            ),

            preferred_chart=plan.get(
                "preferred_chart",
            ),

            confidence=float(
                plan.get(
                    "confidence",
                    1.0,
                )
            ),
        )