from fastapi import APIRouter
from app.api.endpoints.health import router as health_router
from app.api.endpoints.upload import router as upload_router
from app.api.endpoints.analyze import router as analyze_router
from app.api.endpoints.history import router as history_router
from app.api.endpoints.auth import router as auth_router

router = APIRouter()

router.include_router(health_router, tags=["Health"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(upload_router, prefix="/cases", tags=["Cases"])
router.include_router(analyze_router, prefix="/cases", tags=["Cases"])
router.include_router(history_router, prefix="/cases", tags=["Cases"])