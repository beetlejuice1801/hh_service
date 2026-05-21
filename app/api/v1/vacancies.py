import logging

from fastapi import APIRouter, status
from typing import Literal
import asyncio

from repository import TokenRepository, VacancyRepository
from collectors import HHVacancyCollector
from config.settings import settings
from schemas import VacancySchema, VacancyResponse, StatsResponse

log = logging.getLogger(__name__)

router = APIRouter(prefix="/vacancies", tags=["vacancies"])


@router.get("/collect/")
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
            vacancy_schema = VacancySchema(**vacancy, raw_data=vacancy)
            await vacancy_repo.update_vacancy(
                vacancy_schema,
                vacancy_schema.employer,
            )
    return f"Вакансии успешно сохранены. {status.HTTP_200_OK}"


@router.get("/sorted/", response_model=list[VacancyResponse])
async def get_sorted_vacancies(
    salary_from: int = None,
    salary_to: int = None,
    name: str = None,
    experience: str = None,
    order_by: Literal[
        "published_at",
        "salary_from",
        "salary_to",
        "name",
        "experience",
    ] = "published_at",
    order_direction: Literal[
        "asc",
        "desc",
    ] = "desc",
):
    vacancy_repo = await VacancyRepository.get_vacancies(
        salary_from=salary_from,
        salary_to=salary_to,
        name=name,
        experience=experience,
        order_by=order_by,
        order_direction=order_direction,
    )

    return vacancy_repo


@router.get("/stats/")
async def get_vacancies_stats() -> dict:
    median_salary_task = VacancyRepository.get_median_salary()
    frequency_distribution_task = VacancyRepository.frequency_distribution()
    median, distribution = await asyncio.gather(
        median_salary_task,
        frequency_distribution_task,
    )
    result = {
        "median_salary": median,
        "frequency_distribution": distribution,
    }
    return result


@router.get("/{id}/")
async def get_vacancy(id_: str) -> dict:
    vacancy_by_id = await VacancyRepository.get_vacancy_by_id(id_)
    return vacancy_by_id
