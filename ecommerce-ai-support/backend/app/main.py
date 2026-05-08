from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api import chat, orders, escalations, health
from app.config import Settings
import logging

settings = Settings()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up E-Commerce AI Support Agent...")
    yield
    # Shutdown
    logger.info("Shutting down...")

app = FastAPI(
    title="E-Commerce AI Support Agent",
    version="1.0.0",
    description="AI-powered customer support system with RAG and escalation",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(orders.router, prefix="/api/v1/orders", tags=["orders"])
app.include_router(escalations.router, prefix="/api/v1/escalations", tags=["escalations"])
app.include_router(health.router, tags=["health"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "E-Commerce AI Support Agent"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
