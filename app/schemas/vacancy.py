"""
Модуль с pydantic-схемами для валидации данных вакансии в ответах от API.
Необходимо для дальнейшей фильтрации пользователем по критериям вакансии.
Критерии могут дополняться написанием новой схемы.

"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class SalarySchema(BaseModel):
    """
    Схема для заработной платы.

    Attributes:
        from_: Зарплата от
        to: Зарплата до
        currency: Валюта

    """

    from_: int | None = Field(
        None,
        alias="from",
    )
    to: int | None = None
    currency: str | None = None


class EmployerSchema(BaseModel):
    """
    Схема для работодателя.

    Attributes:
        name: Название компании

    """

    id: str | None = None
    name: str | None = None
    url: str | None = None
    alternate_url: str | None = None


class AreaSchema(BaseModel):
    """
    Территориальное расположение.

    Attributes:
        name: Город

    """

    id: str
    name: str
    url: str | None = None


class SnippetSchema(BaseModel):
    """
    Описание требований и обязанностей.

    Attributes:
        requirement: Требования от кандидата
        responsibility: Обязанности позиции

    """

    requirement: str | None
    responsibility: str | None


class ExperienceSchema(BaseModel):
    """
    Требуемый опыт.

    Attributes:
        name: Требуемый опыт

    """

    id: str
    name: str | None = None


class VacancySchema(BaseModel):
    """Полная схема вакансии от API HeadHunter."""

    id: str
    name: str
    area: AreaSchema
    salary: SalarySchema | None = None
    snippet: SnippetSchema | None = None
    experience: ExperienceSchema | None = None
    employer: EmployerSchema
    published_at: datetime
    archived: bool | None = None
    raw_data: dict | None = None


class VacancyResponse(BaseModel):
    """Схема ответа для выдачи вакансий пользователю (фильтрованная)."""

    id: str
    name: str
    employer_id: str | None
    area: str | None
    salary_from: int | None
    salary_to: int | None
    experience: str | None
    snippet_requirement: str | None
    snippet_responsibility: str | None
    published_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StatsResponse(BaseModel):
    """Схема ответа со статистикой по вакансиям."""

    median_salary: dict | None
    frequency_distribution: dict | None
