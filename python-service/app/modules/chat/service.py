from app.modules.eda.services.analysis.planner import AnalysisPlanner
from app.modules.eda.services.analysis.executor import AnalysisExecutor
from app.utils.s3 import load_dataframe_from_s3

planner = AnalysisPlanner()
executor = AnalysisExecutor()


class ChatService:

    async def plan(self, request):
        print("Planning...")
        plan = await planner.plan(
            question=request.question,
            dataset_name=request.dataset_name,
            dataset_profile=request.dataset_profile,
            column_metadata=request.column_metadata,
            dataset_summary=request.dataset_summary,
            correlations=request.correlations,
            existing_charts=request.existing_charts,
        )
        print("plan: ", plan)

        df = await load_dataframe_from_s3(
            request.s3_key
        )
        print(df.shape)

        print("Executing")


        result = await executor.execute(
            df=df,
            plan=plan,
            request=request,
        )

        return result