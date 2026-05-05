from fastapi import APIRouter

from api.v1.auth_and_tokens import router as api_router

router = APIRouter()

router.include_router(api_router)
