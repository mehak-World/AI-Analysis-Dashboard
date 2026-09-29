from app.core.gemini import ask_gemini

from app.modules.eda.services.charts.generator import generate_charts

from .planner import build_composition_plan
from .statistics import generate_composition_statistics
from .chart_builder import build_chart_spec
from .evidence import build_composition_evidence
from .prompts import build_composition_prompt

import json
import re


def extract_json(text):

    text = text.replace("```json", "")
    text = text.replace("```", "").strip()

    match = re.search(r"\{[\s\S]*\}", text)

    if not match:
        raise ValueError("No JSON found.")

    return json.loads(match.group())


async def analyze_composition(
    df,
    user_question,
    category,
    second_entity=None,
):

    print("========== COMPOSITION ==========")

    print("1. Building composition plan")
    composition_plan = build_composition_plan(
        df,
        category,
        second_entity,
    )

    print(composition_plan)

    print("2. Computing statistics")
    statistics = generate_composition_statistics(
        df,
        composition_plan,
    )

    print(statistics)

    print("3. Building chart spec")
    chart_spec = build_chart_spec(
        composition_plan,
    )

    print(chart_spec)

    print("4. Generating charts")
    charts = generate_charts(
        df,
        [chart_spec],
    )

    print(f"Generated {len(charts)} charts")

    print("5. Building evidence")
    evidence = build_composition_evidence(
        composition_plan,
        statistics,
    )

    print(evidence)

    print("6. Building Gemini prompt")
    prompt = build_composition_prompt(
        question=user_question,
        composition_plan=composition_plan,
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