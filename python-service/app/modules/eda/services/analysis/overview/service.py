from app.core.gemini import ask_gemini

from .planner import build_overview_plan
from .statistics import generate_overview_statistics
from .evidence import build_overview_evidence
from .prompts import build_overview_prompt

import json
import re


def extract_json(text):

    text = text.replace("```json", "")
    text = text.replace("```", "").strip()

    match = re.search(r"\{[\s\S]*\}", text)

    if not match:
        raise ValueError("No JSON found.")

    return json.loads(match.group())


async def analyze_overview(
    df,
    user_question,
):

    print("========== OVERVIEW ==========")

    print("1. Building overview plan")
    overview_plan = build_overview_plan(df)

    print(overview_plan)

    print("2. Computing statistics")
    statistics = generate_overview_statistics(
        df,
        overview_plan,
    )

    print(statistics)

    print("3. Building evidence")
    evidence = build_overview_evidence(
        overview_plan,
        statistics,
    )

    print(evidence)

    print("4. Building Gemini prompt")
    prompt = build_overview_prompt(
        question=user_question,
        evidence=evidence,
        statistics=statistics,
    )

    print("5. Calling Gemini")

    response = await ask_gemini(prompt)

    print("Gemini responded")

    print("6. Parsing JSON")

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
        "chart": None,
        "statistics": statistics,
        "evidence": evidence,
        "summary": ai["summary"],
        "insight": ai["insight"],
        "recommendations": ai["recommendations"],
    }