from app.core.gemini import ask_gemini

from app.modules.eda.services.charts.generator import generate_charts

from .planner import build_comparison_plan
from .statistics import generate_comparison_statistics
from .chart_builder import build_chart_spec
from .evidence import build_comparison_evidence
from .prompts import build_comparison_prompt

import json
import re


def extract_json(text):
    text = text.replace("```json", "")
    text = text.replace("```", "").strip()

    match = re.search(
        r"\{[\s\S]*\}",
        text,
    )

    if not match:
        raise ValueError("No JSON found.")

    return json.loads(match.group())


async def analyze_comparison(
    df,
    user_question,
    x,
    y,
):

    # ------------------------
    # Plan
    # ------------------------

    print("========== COMPARISON ==========")

    print("1. Building comparison plan")

    comparison_plan = build_comparison_plan(
        df,
        x,
        y,
    )

    print(comparison_plan)

    # ------------------------
    # Statistics
    # ------------------------

    print("2. Computing statistics")

    statistics = generate_comparison_statistics(
        df,
        comparison_plan,
    )

    print(statistics)

    # ------------------------
    # Chart
    # ------------------------

    print("3. Building chart spec")

    chart_spec = build_chart_spec(
        comparison_plan,
        statistics
    )

    print(chart_spec)

    print("4. Generating charts")

    charts = generate_charts(
        df,
        [chart_spec],
    )

    print(
        f"Generated {len(charts)} charts"
    )

    # ------------------------
    # Evidence
    # ------------------------

    print("5. Building evidence")

    evidence = build_comparison_evidence(
        comparison_plan,
        statistics,
    )

    print(evidence)

    # ------------------------
    # Gemini Prompt
    # ------------------------

    print("6. Building Gemini prompt")

    prompt = build_comparison_prompt(
        question=user_question,
        comparison_plan=comparison_plan,
        evidence=evidence,
        statistics=statistics,
        chart=charts[0] if charts else {},
    )

    # ------------------------
    # Gemini
    # ------------------------

    print("7. Calling Gemini")

    response = await ask_gemini(prompt)

    print("Gemini responded")

    # ------------------------
    # Parse JSON
    # ------------------------

    print("8. Parsing JSON")

    try:

        ai = extract_json(response)

    except Exception:

        ai = {
            "summary": response,
            "insight": "",
            "recommendations": [],
        }

    print(ai)

    print("========== DONE ==========")

    return {
        "chart": charts[0] if charts else None,

        "statistics": statistics,

        "evidence": evidence,

        "summary": ai["summary"],

        "insight": ai["insight"],

        "recommendations": ai["recommendations"],
    }