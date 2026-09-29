from app.modules.eda.services.analysis.models import (
    ExecutionResult,
)

from app.modules.eda.services.analysis.trend.service import (
    analyze_trend,
)


async def execute(
    df,
    plan,
    request,
):

    print(
        "[TREND] Handler started"
    )

    print(
        f"[TREND] Entities: {plan.entities}"
    )

    if len(plan.entities) < 2:
        raise ValueError(
            "Trend analysis requires at least two entities."
        )

    print(
        "[TREND] Calling trend service"
    )

    # --------------------------------------------------
    # Read optional trend configuration
    # --------------------------------------------------

    aggregation = getattr(
        plan,
        "aggregation",
        "mean",
    )

    frequency = getattr(
        plan,
        "frequency",
        "day",
    )

    analysis_type = getattr(
        plan,
        "analysis_type",
        "time_series",
    )

    result = await analyze_trend(
        df=df,

        user_question=plan.user_question,

        x=plan.entities[0],

        y=plan.entities[1],

        frequency=frequency,

        analysis_type=analysis_type,
    )

    print(
        "[TREND] Trend service completed"
    )

    return ExecutionResult(

        plan=plan,

        charts=(
            [result["chart"]]
            if result.get("chart")
            else []
        ),

        statistics=result[
            "statistics"
        ],

        evidence=result[
            "evidence"
        ],

        explanation=result[
            "summary"
        ],

        recommendations=result[
            "recommendations"
        ],
    )