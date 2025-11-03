from fastapi import APIRouter


router = APIRouter()


@router.get("/metrics", tags=["health"])
async def get_metrics():
    """
    Simple metrics endpoint to indicate the service is alive.
    Can be expanded to expose more detailed application metrics.
    """
    return {"status": "ok"}
