import logging

from fastapi import APIRouter
from typing import Literal
import asyncio

from repository import TokenRepository, VacancyRepository
from collectors import HHVacancyCollector
from config.settings import settings
from schemas import VacancySchema, VacancyResponse

log = logging.getLogger(__name__)

router = APIRouter(prefix="/vacancies", tags=["vacancies"])


@router.get("/collect/")
async def collect_vacancies(text, area) -> list[dict[str, any]]:
    """
    Эндпоинт для сбора вакансий с HeadHunter.

    Выполняет сбор вакансий по заданным критериям поиска,
    сохраняет их в базу данных и возвращает собранные данные.

    Args:
        text (str): Поисковый запрос (например, "Python developer")
        area (int): ID региона (например, 1 - Москва, 2 - Санкт-Петербург)

    Returns:
        Список собранных вакансий в исходном формате
    """
    token_repo = TokenRepository()
    vacancy_repo = VacancyRepository()
    collector = HHVacancyCollector(
        access_token=await token_repo.get_token(
            settings.app.user_id.get_secret_value(),
            token_type="access_token",
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
            if not vacancy_schema.employer or not vacancy_schema.employer.id:
                continue
            await vacancy_repo.update_vacancy(
                vacancy_schema,
                vacancy_schema.employer,
            )
    return all_vacancies


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
) -> list[VacancyResponse]:
    """
    Эндпоинт для получения отфильтрованных и отсортированных вакансий из БД.

    Поддерживает фильтрацию по зарплате, названию и опыту,
    а также сортировку по различным полям.

    Args:
        salary_from: Нижняя граница зарплаты
        salary_to: Верхняя граница зарплаты
        name: Часть названия вакансии
        experience: Требуемый опыт работы
        order_by: Поле для сортировки
        order_direction: Направление сортировки

    Returns:
        list[VacancyResponse]: Список вакансий, соответствующих критериям
    """
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
    """
    Эндпоинт для получения статистики по вакансиям.

    Параллельно вычисляет медианную зарплату и распределение по опыту
    для построения аналитических отчетов.

    Returns:
        Словарь со статистикой:
            - median_salary: Медианная зарплата
            - frequency_distribution: Распределение по опыту
    """
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


@router.get("/{id}/", response_model=VacancyResponse)
async def get_vacancy(id_: str) -> dict:
    """
    Эндпоинт для получения конкретной вакансии по её ID.

    Args:
        id_ (str): Уникальный идентификатор вакансии в формате UUID

    Returns:
        VacancyResponse: Данные вакансии в формате ответа

    """
    vacancy_by_id = await VacancyRepository.get_vacancy_by_id(id_)
    return vacancy_by_id
