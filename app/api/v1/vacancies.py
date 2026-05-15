from fastapi import APIRouter

from repository import TokenRepository, VacancyRepository
from collectors import HHVacancyCollector
from config.settings import settings
from schemas import VacancySchema

router = APIRouter(prefix="/vacancies", tags=["vacancies"])


@router.get("/collect")
async def collect_vacancies(text, area):
    token_repo = TokenRepository()
    vacancy_repo = VacancyRepository()
    collector = HHVacancyCollector(
        access_token=await token_repo.get_token(
            settings.app.user_id.get_secret_value(),
        )
    )
    params = {
        "text": text,
        "area": area,
    }
    async with collector as collector:
        all_vacancies = await collector.fetch_vacancies(params=params)

        for vacancy in all_vacancies:
            vacancy_schema = VacancySchema(**vacancy)
            await vacancy_repo.update_vacancy(
                vacancy_schema,
                vacancy_schema.employer,
            )
    return True
