from .registry import HANDLERS


class AnalysisExecutor:

    async def execute(
        self,
        df,
        plan,
        request=None,
    ):

        print("=" * 60)
        print("[EXECUTOR] Starting execution")
        print(f"[EXECUTOR] Intent: {plan.intent}")
        print(f"[EXECUTOR] Entities: {plan.entities}")
        print(f"[EXECUTOR] DataFrame shape: {df.shape}")
        print("=" * 60)

        handler = HANDLERS.get(plan.intent)

        if handler is None:
            raise ValueError(
                f"No handler registered for intent '{plan.intent.value}'."
            )

        print(f"[EXECUTOR] Using handler: {handler.__module__}")

        result = await handler(
            df=df,
            plan=plan,
            request=request,
        )

        print("[EXECUTOR] Handler completed successfully")

        return result