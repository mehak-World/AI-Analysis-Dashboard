from fastapi import APIRouter, HTTPException
import traceback
from .schema import InsightsRequest
from app.modules.ai.service import run_insights

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/insights")
async def insights(body: InsightsRequest):
    try:
        data = await run_insights(
            dataset_name=body.dataset_name,
            profile=body.profile,
            charts=body.charts,
        )

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