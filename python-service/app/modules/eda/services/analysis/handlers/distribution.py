from app.modules.eda.services.analysis.models import (
    ExecutionResult,
)

from app.modules.eda.services.analysis.distribution.service import (
    analyze_distribution,
)


async def execute(
    df,
    plan,
    request,
):

    print("[DISTRIBUTION] Handler started")

    print(f"[DISTRIBUTION] Entities: {plan.entities}")

    if len(plan.entities) < 1:
        raise ValueError(
            "Distribution analysis requires at least one entity."
        )

    print("[DISTRIBUTION] Calling distribution service")

    result = await analyze_distribution(
        df=df,
        user_question=plan.user_question,
        column=plan.entities[0],
    )

    print("[DISTRIBUTION] Distribution service completed")

    return ExecutionResult(
        plan=plan,
        charts=[result["chart"]],
        statistics=result["statistics"],
        evidence=result["evidence"],
        explanation=result["summary"],
        recommendations=result["recommendations"],
    )