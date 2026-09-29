from app.modules.eda.services.analysis.models import (
    ExecutionResult,
)

from app.modules.eda.services.analysis.overview.service import (
    analyze_overview,
)


async def execute(
    df,
    plan,
    request,
):

    print("[OVERVIEW] Handler started")

    print("[OVERVIEW] Calling overview service")

    result = await analyze_overview(
        df=df,
        user_question=plan.user_question,
    )

    print("[OVERVIEW] Overview service completed")

    return ExecutionResult(
        plan=plan,
        charts=[result["chart"]] if result["chart"] else [],
        statistics=result["statistics"],
        evidence=result["evidence"],
        explanation=result["summary"],
        recommendations=result["recommendations"],
    )