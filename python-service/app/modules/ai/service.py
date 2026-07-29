import json

from app.core.gemini import ask_gemini
from .prompts import build_insights_prompt
import re


def extract_json(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found.")
    return json.loads(match.group())


async def run_insights(
    dataset_name: str,
    profile: dict,
    charts: list,
):

    prompt = build_insights_prompt(
        dataset_name=dataset_name,
        profile=profile,
        charts=charts,
    )

    response = await ask_gemini(prompt)

    return extract_json(response)