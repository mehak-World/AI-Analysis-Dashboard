"""
Gemini-based candidate ranking.

Replaces the keyword-list scorer for *ranking* while keeping candidate
generation exactly as it was: candidates are already guaranteed
structurally valid (real columns, real enum values) before they ever
reach Gemini, so the model is asked to rank a fixed list by index, not
to invent chart specs. Gemini can only return an index into a list you
already built plus a score — hallucinating a nonexistent chart isn't a
failure mode here. The worst case is a malformed or unusable response,
which is handled by falling back to the heuristic scorer.

Every fallback path in this module is deliberate: if Gemini is slow,
over quota, or returns something unparseable, ranking silently
degrades to the rule-based score already computed for it — the
pipeline never breaks because of an AI outage.
"""
import json
import re
from typing import Dict, List, Optional

from .classifier import DatasetType
from .models import ChartSpec
from .scorer import score_candidates

from app.core.gemini import ask_gemini

# Cap how many candidates get sent to Gemini per call. Wide datasets can
# produce 100+ structurally valid candidates; sending all of them means
# an oversized prompt and a slow/expensive call for candidates that
# would never survive selection anyway. Pre-filter to the heuristic
# top-N first, then let Gemini re-rank just that shortlist.
MAX_CANDIDATES_FOR_AI_RANKING = 20

# If Gemini returns valid scores for fewer than this fraction of the
# shortlist, treat the whole response as untrustworthy rather than
# half-merging it — a mostly-broken response is a sign something went
# wrong with the call, not that half the candidates are just unranked.
MIN_VALID_FRACTION = 0.5


async def rank_candidates_with_gemini(
    candidates: List[ChartSpec],
    dataset_type: DatasetType,
    max_candidates: int = MAX_CANDIDATES_FOR_AI_RANKING,
) -> List[ChartSpec]:
    """
    Scores candidates with the rule-based scorer first (baseline and
    fallback), then asks Gemini to re-rank the top `max_candidates` of
    those by business relevance and rewrite their reason text. Any
    candidate Gemini doesn't return a valid score for keeps its
    heuristic score untouched.
    """
    scored = score_candidates(candidates)

    if not scored:
        return scored

    shortlist = sorted(scored, key=lambda c: c.priority, reverse=True)[:max_candidates]
    if not shortlist:
        return scored

    response = await ask_gemini(_build_prompt(shortlist, dataset_type))

    print("response: ", response)
    rankings = _safe_parse_rankings(response, expected_count=len(shortlist))

    if rankings is None:
        # Gemini call failed, timed out, or returned something we can't
        # trust — keep the heuristic scores as-is. Pipeline stays correct.
        return scored

    for i, chart in enumerate(shortlist):
        ranking = rankings.get(i)
        if ranking is None:
            continue  # this index was missing/invalid — keep heuristic score
        chart.priority = ranking["score"]
        if ranking["reason"]:
            chart.reason = ranking["reason"]

    return scored


def _build_prompt(candidates: List[ChartSpec], dataset_type: DatasetType) -> str:
    lines = []
    for i, c in enumerate(candidates):
        x = c.x.column if c.x else None
        y = c.y.column if c.y else None
        lines.append(
            f'{i}: type={c.chart_type.value}, x={x}, y={y}, '
            f'aggregation={c.aggregation.value}, '
            f'rule_based_score={c.priority}, '
            f'current_reason="{c.reason}"'
        )

    candidate_block = "\n".join(lines)

    return (
        f"Dataset type: {dataset_type.value}.\n"
        "You are ranking candidate charts for a business analytics "
        "dashboard. Each candidate below already references real "
        "columns and a valid chart type — your job is ONLY to judge "
        "business relevance, not to invent or modify columns.\n\n"
        f"Candidates:\n{candidate_block}\n\n"
        "For EVERY candidate index above, return a business-relevance "
        "score from 0-100 and a rewritten one-sentence reason (max 20 "
        "words, business-facing, no jargon). Return ONLY a JSON array, "
        "no markdown, no preamble, in this exact shape:\n"
        '[{"index": 0, "score": 82, "reason": "..."}, ...]\n'
        f"The array MUST contain exactly {len(candidates)} objects, one "
        "per candidate index, with no duplicates and no indices outside "
        f"0-{len(candidates) - 1}."
    )


def _safe_parse_rankings(
    text: str,
    expected_count: int,
) -> Optional[Dict[int, dict]]:
    """
    Returns {index: {"score": int, "reason": str}} on a usable
    response, or None if the response can't be trusted (not JSON,
    wrong shape, or too few valid entries to be worth merging).
    """
    if not text:
        return None

    cleaned = re.sub(r"^```json|```$", "", text.strip(), flags=re.MULTILINE).strip()

    try:
        parsed = json.loads(cleaned)
    except (json.JSONDecodeError, TypeError):
        return None

    if not isinstance(parsed, list):
        return None

    rankings: Dict[int, dict] = {}
    for item in parsed:
        if not isinstance(item, dict):
            continue

        index = item.get("index")
        score = item.get("score")

        if not isinstance(index, int) or index < 0 or index >= expected_count:
            continue
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            continue

        rankings[index] = {
            "score": max(0, min(100, int(score))),
            "reason": str(item.get("reason", "")).strip(),
        }

    if len(rankings) < expected_count * MIN_VALID_FRACTION:
        return None

    return rankings