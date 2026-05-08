from fastapi import APIRouter
from app.models.schemas import HealthResponse
from datetime import datetime

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.utcnow()
    )

@router.get("/ready")
async def readiness_check():
    """
    Readiness check endpoint for Kubernetes
    """
    return {
        "status": "ready",
        "message": "Service is ready to accept requests"
    }

@router.get("/live")
async def liveness_check():
    """
    Liveness check endpoint for Kubernetes
    """
    return {
        "status": "alive",
        "message": "Service is running"
    }
