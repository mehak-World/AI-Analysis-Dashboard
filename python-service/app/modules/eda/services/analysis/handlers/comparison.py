from app.modules.eda.services.analysis.models import (
    ExecutionResult,
)

from app.modules.eda.services.analysis.comparison.service import (
    analyze_comparison,
)


async def execute(
    df,
    plan,
    request,
):

    print("[COMPARISON] Handler started")

    print(
        f"[COMPARISON] Entities: {plan.entities}"
    )

    if len(plan.entities) < 2:
        raise ValueError(
            "Comparison analysis requires at least two entities."
        )

    print(
        "[COMPARISON] Calling comparison service"
    )

    result = await analyze_comparison(
        df=df,
        user_question=plan.user_question,
        x=plan.entities[0],
        y=plan.entities[1],
    )

    print(
        "[COMPARISON] Comparison service completed"
    )

    return ExecutionResult(
        plan=plan,
        charts=[result["chart"]],
        statistics=result["statistics"],
        evidence=result["evidence"],
        explanation=result["summary"],
        recommendations=result["recommendations"],
    )