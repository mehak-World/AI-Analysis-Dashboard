import re

from app.modules.eda.services.analysis.models import (
    ExecutionResult,
)

from app.modules.eda.services.analysis.ranking.service import (
    analyze_ranking,
)


BOTTOM_KEYWORDS = ("bottom", "least", "lowest", "worst", "smallest")


def _extract_top_n(question: str, default: int = 10) -> int:

    match = re.search(r"\b(top|bottom)\s+(\d+)\b", question.lower())

    if match:
        return int(match.group(2))

    return default


def _extract_order(question: str, default: str = "desc") -> str:

    lowered = question.lower()

    if any(keyword in lowered for keyword in BOTTOM_KEYWORDS):
        return "asc"

    return default


async def execute(
    df,
    plan,
    request,
):

    print("[RANKING] Handler started")

    print(f"[RANKING] Entities: {plan.entities}")

    if len(plan.entities) < 1:
        raise ValueError(
            "Ranking analysis requires at least one entity."
        )

    category = plan.entities[0]
    value = plan.entities[1] if len(plan.entities) > 1 else None

    top_n = _extract_top_n(plan.user_question)
    order = _extract_order(plan.user_question)

    print(f"[RANKING] top_n={top_n}, order={order}")

    print("[RANKING] Calling ranking service")

    result = await analyze_ranking(
        df=df,
        user_question=plan.user_question,
        category=category,
        value=value,
        top_n=top_n,
        order=order,
    )

    print("[RANKING] Ranking service completed")

    return ExecutionResult(
        plan=plan,
        charts=[result["chart"]],
        statistics=result["statistics"],
        evidence=result["evidence"],
        explanation=result["summary"],
        recommendations=result["recommendations"],
    )