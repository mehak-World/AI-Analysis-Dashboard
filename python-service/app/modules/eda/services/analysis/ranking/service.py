from app.core.gemini import ask_gemini

from app.modules.eda.services.charts.generator import generate_charts

from .planner import build_ranking_plan
from .statistics import generate_ranking_statistics
from .chart_builder import build_chart_spec
from .evidence import build_ranking_evidence
from .prompts import build_ranking_prompt

import json
import re


def extract_json(text):

    text = text.replace("```json", "")
    text = text.replace("```", "").strip()

    match = re.search(r"\{[\s\S]*\}", text)

    if not match:
        raise ValueError("No JSON found.")

    return json.loads(match.group())


async def analyze_ranking(
    df,
    user_question,
    category,
    value=None,
    top_n=10,
    order="desc",
):

    # ------------------------
    # Plan
    # ------------------------

    print("========== RANKING ==========")

    print("1. Building ranking plan")
    ranking_plan = build_ranking_plan(
        df,
        category,
        value,
        top_n,
        order,
    )

    print(ranking_plan)

    print("2. Computing statistics")
    statistics = generate_ranking_statistics(
        df,
        ranking_plan,
    )

    print(statistics)

    print("3. Building chart spec")
    chart_spec = build_chart_spec(
        ranking_plan,
    )

    print(chart_spec)

    print("4. Generating charts")
    charts = generate_charts(
        df,
        [chart_spec],
    )

    print(f"Generated {len(charts)} charts")

    print("5. Building evidence")
    evidence = build_ranking_evidence(
        ranking_plan,
        statistics,
    )

    print(evidence)

    print("6. Building Gemini prompt")
    prompt = build_ranking_prompt(
        question=user_question,
        ranking_plan=ranking_plan,
        evidence=evidence,
        statistics=statistics,
        chart=charts[0] if charts else {},
    )

    print("7. Calling Gemini")

    response = await ask_gemini(prompt)

    print("Gemini responded")

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