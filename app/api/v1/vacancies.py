from fastapi import APIRouter, status

from repository import TokenRepository

router = APIRouter(prefix="/vacancies", tags=["vacancies"])


@router.get("/collect")
async def collect_vacancies(text, area):
    pass
