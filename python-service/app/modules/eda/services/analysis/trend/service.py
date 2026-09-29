"""
Trend analysis service.

Coordinates:

Planner
→ Statistics
→ ChartSpec
→ Chart generation
→ Evidence
→ Gemini explanation
"""

import json
import re

from app.core.gemini import ask_gemini
from app.modules.eda.services.charts.generator import (
    generate_charts,
)

from .planner import build_trend_plan
from .statistics import generate_trend_statistics
from .chart_builder import build_chart_spec
from .evidence import build_trend_evidence
from .prompt import build_trend_prompt


def extract_json(text):

    text = text.replace(
        "```json",
        "",
    )

    text = text.replace(
        "```",
        "",
    ).strip()

    match = re.search(
        r"\{[\s\S]*\}",
        text,
    )

    if not match:
        raise ValueError(
            "No JSON found."
        )

    return json.loads(
        match.group()
    )


async def analyze_trend(
    df,
    user_question,
    x,
    y,
    frequency="day",
    analysis_type="time_series",
):

    print(
        "========== TREND =========="
    )

    # --------------------------------------------------
    # Plan
    # --------------------------------------------------

    print(
        "1. Building trend plan"
    )

    trend_plan = build_trend_plan(
        df=df,
        x=x,
        y=y,
        frequency=frequency,
        analysis_type=analysis_type,
    )

    print(trend_plan)

    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    print(
        "2. Computing statistics"
    )

    statistics = (
        generate_trend_statistics(
            df,
            trend_plan,
        )
    )

    print(statistics)

    # --------------------------------------------------
    # Chart Spec
    # --------------------------------------------------

    print(
        "3. Building chart spec"
    )

    chart_spec = build_chart_spec(
        trend_plan,
    )

    print(chart_spec)

    # --------------------------------------------------
    # Charts
    # --------------------------------------------------

    print(
        "4. Generating charts"
    )

    charts = generate_charts(
        df,
        [chart_spec],
    )

    print(
        f"Generated {len(charts)} charts"
    )

    # --------------------------------------------------
    # Evidence
    # --------------------------------------------------

    print(
        "5. Building evidence"
    )

    evidence = build_trend_evidence(
        trend_plan,
        statistics,
    )

    print(evidence)

    # --------------------------------------------------
    # Prompt
    # --------------------------------------------------

    print(
        "6. Building Gemini prompt"
    )

    prompt = build_trend_prompt(
        question=user_question,

        trend_plan=trend_plan,

        evidence=evidence,

        statistics=statistics,

        chart=(
            charts[0]
            if charts
            else {}
        ),
    )

    # --------------------------------------------------
    # Gemini
    # --------------------------------------------------

    print(
        "7. Calling Gemini"
    )

    response = await ask_gemini(
        prompt
    )

    print(
        "Gemini responded"
    )

    # --------------------------------------------------
    # Parse JSON
    # --------------------------------------------------

    print(
        "8. Parsing JSON"
    )

    try:

        ai = extract_json(
            response
        )

    except Exception:

        ai = {
            "summary": response,
            "insight": "",
            "recommendations": [],
        }

    print(ai)

    print(
        "========== DONE =========="
    )

    return {

        "chart": (
            charts[0]
            if charts
            else None
        ),

        "statistics": statistics,

        "evidence": evidence,

        "summary": ai.get(
            "summary",
            "",
        ),

        "insight": ai.get(
            "insight",
            "",
        ),

        "recommendations": ai.get(
            "recommendations",
            [],
        ),
    }