from app.modules.eda.services.analysis.models import (
    ExecutionResult,
)

from app.modules.eda.services.analysis.composition.service import (
    analyze_composition,
)


async def execute(
    df,
    plan,
    request,
):

    print("[COMPOSITION] Handler started")

    print(f"[COMPOSITION] Entities: {plan.entities}")

    if len(plan.entities) < 1:
        raise ValueError(
            "Composition analysis requires at least one entity."
        )

    category = plan.entities[0]
    second_entity = plan.entities[1] if len(plan.entities) > 1 else None

    print("[COMPOSITION] Calling composition service")

    result = await analyze_composition(
        df=df,
        user_question=plan.user_question,
        category=category,
        second_entity=second_entity,
    )

    print("[COMPOSITION] Composition service completed")

    return ExecutionResult(
        plan=plan,
        charts=[result["chart"]],
        statistics=result["statistics"],
        evidence=result["evidence"],
        explanation=result["summary"],
        recommendations=result["recommendations"],
    )