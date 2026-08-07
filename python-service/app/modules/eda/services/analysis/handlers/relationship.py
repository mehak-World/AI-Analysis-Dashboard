from app.modules.eda.services.analysis.models import (
    ExecutionResult,
)

from app.modules.eda.services.analysis.relationship.service import (
    analyze_relationship,
)


async def execute(
    df,
    plan,
    request,
):

    print("[RELATIONSHIP] Handler started")

    print(f"[RELATIONSHIP] Entities: {plan.entities}")

    if len(plan.entities) < 2:
        raise ValueError(
            "Relationship analysis requires at least two entities."
        )

    print("[RELATIONSHIP] Calling relationship service")

    result = await analyze_relationship(
        df=df,
        user_question=plan.user_question,
        x=plan.entities[0],
        y=plan.entities[1],
    )

    print("[RELATIONSHIP] Relationship service completed")

    return ExecutionResult(
        plan=plan,
        charts=[result["chart"]],
        statistics=result["statistics"],
        evidence=result["evidence"],
        explanation=result["summary"],
        recommendations=result["recommendations"],
    )