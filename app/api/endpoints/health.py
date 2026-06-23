from fastapi import APIRouter
# Assuming you have a settings file somewhere
from app.config import settings 

# Create the router instance
router = APIRouter(prefix="/system", tags=["System"])

@router.get("/health")
async def health():
    return {
        "status": "healthy",
        "version": settings.app_version,
    }
