from app.core.gemini import ask_gemini

from app.modules.eda.services.charts.generator import generate_charts

from .planner import build_relationship_plan
from .statistics import generate_relationship_statistics
from .chart_builder import build_chart_spec
from .evidence import build_relationship_evidence
from .prompts import build_relationship_prompt

import json
import re


def extract_json(text):

    text = text.replace("```json", "")
    text = text.replace("```", "").strip()

    match = re.search(r"\{[\s\S]*\}", text)

    if not match:
        raise ValueError("No JSON found.")

    return json.loads(match.group())


async def analyze_relationship(
    df,
    user_question,
    x,
    y,
):

    # ------------------------
    # Plan
    # ------------------------

    print("========== RELATIONSHIP ==========")

    print("1. Building relationship plan")
    relationship_plan = build_relationship_plan(
        df,
        x,
        y,
    )

    print(relationship_plan)

    print("2. Computing statistics")
    statistics = generate_relationship_statistics(
        df,
        relationship_plan,
    )

    print(statistics)

    print("3. Building chart spec")
    chart_spec = build_chart_spec(
        relationship_plan,
    )

    print(chart_spec)

    print("4. Generating charts")
    charts = generate_charts(
        df,
        [chart_spec],
    )

    print(f"Generated {len(charts)} charts")

    print("5. Building evidence")
    evidence = build_relationship_evidence(
        relationship_plan,
        statistics,
    )

    print(evidence)

    print("6. Building Gemini prompt")
    prompt = build_relationship_prompt(
        question=user_question,
        relationship_plan=relationship_plan,
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

    print("========== DONE ==========")

    return {
        "chart": charts[0] if charts else None,
        "statistics": statistics,
        "evidence": evidence,
        "summary": ai["summary"],
        "insight": ai["insight"],
        "recommendations": ai["recommendations"],
    }