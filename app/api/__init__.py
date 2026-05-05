from fastapi import APIRouter

from api.v1 import router as api_router

router = APIRouter()

router.include_router(api_router)
