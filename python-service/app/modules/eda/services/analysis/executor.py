# from .registry import HANDLERS


# class AnalysisExecutor:

#     async def execute(
#         self,
#         df,
#         plan,
#         request=None,
#     ):

#         print("=" * 60)
#         print("[EXECUTOR] Starting execution")
#         print(f"[EXECUTOR] Intent: {plan.intent}")
#         print(f"[EXECUTOR] Entities: {plan.entities}")
#         print(f"[EXECUTOR] DataFrame shape: {df.shape}")
#         print("=" * 60)

#         handler = HANDLERS.get(plan.intent)

#         if handler is None:
#             raise ValueError(
#                 f"No handler registered for intent '{plan.intent.value}'."
#             )

#         print(f"[EXECUTOR] Using handler: {handler.__module__}")

#         result = await handler(
#             df=df,
#             plan=plan,
#             request=request,
#         )

#         print("[EXECUTOR] Handler completed successfully")

#         return result


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
        print(f"[EXECUTOR] Filters: {plan.filters}")
        print(f"[EXECUTOR] DataFrame shape (before filters): {df.shape}")
        print("=" * 60)

        df = self._apply_filters(df, plan.filters)

        print(f"[EXECUTOR] DataFrame shape (after filters): {df.shape}")

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

    def _apply_filters(self, df, filters):

        if not filters:
            return df

        for column, value in filters.items():

            if column not in df.columns:
                print(f"[EXECUTOR] Filter column '{column}' not found, skipping")
                continue

            if isinstance(value, list):
                df = df[df[column].isin(value)]
            else:
                df = df[df[column] == value]

        return df