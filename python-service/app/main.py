from fastapi import FastAPI
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from app.modules.eda.router import router as eda_router
from app.modules.ai.router import router as ai_router
from app.modules.chat.router import router as chat_router

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

prefix = "/api"
app.include_router(eda_router, prefix=prefix)
app.include_router(ai_router, prefix=prefix)
app.include_router(chat_router, prefix=prefix)

@app.get("/health")
async def health():
    return {"status": "healthy"}