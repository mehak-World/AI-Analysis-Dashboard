import traceback

from fastapi import APIRouter, HTTPException

from .schema import AnalyzeS3Request

from app.utils.s3 import load_dataframe_from_s3

from app.modules.eda.services.profile.profile_service import run_profile
from app.modules.eda.services.charts.chart_service import run_charts

router = APIRouter(prefix="/eda", tags=["EDA"])

@router.post("/profile")
async def profile(body: AnalyzeS3Request):
    try:
        print("req body: ", body)
        df = await load_dataframe_from_s3(body.s3_key)

        data = await run_profile(df)

        return {
            "success": True,
            "session_id": body.session_id,
            "rows": len(df),
            "columns": len(df.columns),
            "data": data,
        }

    except Exception as e:
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

@router.post("/charts")
async def charts(body: AnalyzeS3Request):
    try:
        df = await load_dataframe_from_s3(body.s3_key)

        data = await run_charts(df)

        return {
            "success": True,
            "session_id": body.session_id,
            "data": data,
        }

    except Exception as e:
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
