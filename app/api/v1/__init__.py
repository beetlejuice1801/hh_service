from fastapi import APIRouter

from api.v1.token_retrieval import router as token_router
from api.v1.vacancies import router as vacancies_router

router = APIRouter()

router.include_router(token_router)
router.include_router(vacancies_router)
