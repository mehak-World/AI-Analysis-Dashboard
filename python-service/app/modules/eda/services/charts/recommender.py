"""
High-level chart recommendation orchestration.

Pipeline:
    classify dataset -> detect semantic roles -> generate candidates
    -> score -> select top N -> (optional) enrich reasons + suggest
    follow-up questions via Gemini.

AI enrichment is cosmetic, never load-bearing: chart selection is
fully decided by the rule-based pipeline before Gemini is touched,
so a Gemini outage degrades reason text quality, not correctness.

NOTE: adjust the `ask_gemini` import path below to wherever your
gemini_client actually lives in the project.
"""
import json
import re
from typing import List, Optional

import pandas as pd

from .candidate_generator import generate_candidates
from .classifier import DatasetType, classify_dataset
from .models import ChartSpec
from .scorer import score_candidates
from .selector import select_charts
from .semantic_roles import detect_semantic_roles

from app.core.gemini import ask_gemini


async def recommend_charts(
    df: pd.DataFrame,
    column_metadata: List[dict],
    correlations: List[dict],
    max_charts: int = 10,
    use_ai_enrichment: bool = True,
) -> List[ChartSpec]:

    dataset_type = classify_dataset(column_metadata)
    roles = detect_semantic_roles(df, column_metadata)

    candidates = generate_candidates(roles, correlations)
    if not candidates:
        return []

    scored = score_candidates(candidates)
    selected = select_charts(scored, max_charts=max_charts)

    if use_ai_enrichment and selected:
        selected = await _enrich_with_gemini(selected, dataset_type)

    return selected


async def suggest_followup_questions(
    column_metadata: List[dict],
    dataset_type: Optional[str] = None,
) -> List[str]:
    """
    Uses Gemini to propose natural-language follow-up analysis
    questions a business user could ask next, grounded in the actual
    columns available so it doesn't hallucinate fields that don't
    exist. Maps directly onto `datasetSummary.recommendedQuestions`
    in the Session schema.
    """
    columns_desc = ", ".join(
        f"{c['name']} ({c.get('category', 'unknown')})"
        for c in column_metadata
    )

    prompt = (
        "You are a data analyst assistant. Given a dataset with these "
        f"columns: {columns_desc}"
        f"{f' (dataset type: {dataset_type})' if dataset_type else ''}, "
        "suggest 5 concise, business-relevant analysis questions a user "
        "could ask next. Return ONLY a JSON array of 5 short strings, "
        "no markdown, no preamble."
    )

    response = await ask_gemini(prompt)
    questions = _safe_parse_json_list(response)
    return questions or []


async def _enrich_with_gemini(
    charts: List[ChartSpec],
    dataset_type: DatasetType,
) -> List[ChartSpec]:
    """
    Asks Gemini to rewrite each chart's `reason` as a punchy,
    business-facing one-liner. Falls back to the rule-based reason
    already on the ChartSpec if Gemini fails or returns a mismatched
    count — enrichment can only improve wording, never break output.
    """
    chart_lines = "\n".join(
        f"{i + 1}. type={c.chart_type.value}, "
        f"x={c.x.column if c.x else None}, "
        f"y={c.y.column if c.y else None}, "
        f"current_reason={c.reason}"
        for i, c in enumerate(charts)
    )

    prompt = (
        f"Dataset type: {dataset_type.value}.\n"
        f"Here are {len(charts)} charts selected for a business "
        f"dashboard:\n{chart_lines}\n\n"
        "Rewrite each chart's reason as one short, business-facing "
        "sentence (max 20 words) explaining why a business user should "
        "care. Return ONLY a JSON array of strings in the same order, "
        "no markdown, no preamble."
    )

    response = await ask_gemini(prompt)
    reasons = _safe_parse_json_list(response)

    if len(reasons) == len(charts):
        for chart, reason in zip(charts, reasons):
            chart.reason = reason
    # else: keep the rule-based reasons already on each ChartSpec

    return charts


def _safe_parse_json_list(text: str) -> List[str]:
    if not text:
        return []

    cleaned = re.sub(r"^```json|```$", "", text.strip(), flags=re.MULTILINE).strip()

    try:
        parsed = json.loads(cleaned)
        if isinstance(parsed, list):
            return [str(item) for item in parsed]
    except (json.JSONDecodeError, TypeError):
        pass

    return []

# """
# High-level chart recommendation orchestration.

# Pipeline:
#     classify dataset -> detect semantic roles -> generate candidates
#     -> rank (Gemini, falling back to the rule-based scorer) -> select
#     top N.

# Ranking can never break candidate correctness: generate_candidates
# already guarantees every candidate references a real column and a
# valid enum value, so whether Gemini or the heuristic scorer decides
# the ordering, the *set* of possible outputs is identical — only the
# priority attached to each one changes.

# NOTE: adjust the `ask_gemini` import path below to wherever your
# gemini_client actually lives in the project.
# """
# import json
# import re
# from typing import List, Optional

# import pandas as pd

# from .candidate_generator import generate_candidates
# from .classifier import classify_dataset
# from .gemini_scorer import rank_candidates_with_gemini
# from .models import ChartSpec
# from .selector import select_charts
# from .semantic_roles import detect_semantic_roles

# # TODO: point this at your actual gemini_client module
# from app.core.gemini import ask_gemini


# async def recommend_charts(
#     df: pd.DataFrame,
#     column_metadata: List[dict],
#     correlations: List[dict],
#     max_charts: int = 10,
#     use_ai_ranking: bool = True,
# ) -> List[ChartSpec]:

#     dataset_type = classify_dataset(column_metadata)
#     roles = detect_semantic_roles(df, column_metadata)

#     candidates = generate_candidates(roles, correlations)
#     if not candidates:
#         return []

#     if use_ai_ranking:
#         scored = await rank_candidates_with_gemini(candidates, dataset_type)
#     else:
#         # Kept for local dev / cost-sensitive runs — same candidates,
#         # just skips the Gemini call and uses the rule-based scores.
#         from .scorer import score_candidates
#         scored = score_candidates(candidates)

#     return select_charts(scored, max_charts=max_charts)


# async def suggest_followup_questions(
#     column_metadata: List[dict],
#     dataset_type: Optional[str] = None,
# ) -> List[str]:
#     """
#     Uses Gemini to propose natural-language follow-up analysis
#     questions a business user could ask next, grounded in the actual
#     columns available so it doesn't hallucinate fields that don't
#     exist. Maps directly onto `datasetSummary.recommendedQuestions`
#     in the Session schema.
#     """
#     columns_desc = ", ".join(
#         f"{c['name']} ({c.get('category', 'unknown')})"
#         for c in column_metadata
#     )

#     prompt = (
#         "You are a data analyst assistant. Given a dataset with these "
#         f"columns: {columns_desc}"
#         f"{f' (dataset type: {dataset_type})' if dataset_type else ''}, "
#         "suggest 5 concise, business-relevant analysis questions a user "
#         "could ask next. Return ONLY a JSON array of 5 short strings, "
#         "no markdown, no preamble."
#     )

#     response = await ask_gemini(prompt)
#     return _safe_parse_json_list(response)


# def _safe_parse_json_list(text: str) -> List[str]:
#     if not text:
#         return []

#     cleaned = re.sub(r"^```json|```$", "", text.strip(), flags=re.MULTILINE).strip()

#     try:
#         parsed = json.loads(cleaned)
#         if isinstance(parsed, list):
#             return [str(item) for item in parsed]
#     except (json.JSONDecodeError, TypeError):
#         pass

#     return []