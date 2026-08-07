from fastapi import APIRouter

from .service import ChatService
from .schema import PlannerRequest

router = APIRouter(prefix="/chat", tags=["chat"])

chat_service = ChatService()


@router.post("/plan")
async def plan(request: PlannerRequest):
    return await chat_service.plan(request)