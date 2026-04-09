"""
Модуль с pydantic-схемами для валидации данных вакансии в ответах от API.
Необходимо для дальнейшей фильтрации пользователем по критериям вакансии.
Критерии могут дополняться написанием новой схемы.

"""

from pydantic import BaseModel, Field
from datetime import datetime


class Salary(BaseModel):
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


class Employer(BaseModel):
    """
    Схема для работодателя.

    Attributes:
        name: Название компании

    """

    id: str
    name: str
    url: str | None = None
    alternate_url: str | None = None
    trusted: bool


class Area(BaseModel):
    """
    Территориальное расположение.

    Attributes:
        name: Город

    """

    id: str
    name: str
    url: str | None = None


class VacancyBrief(BaseModel):
    """
    Описание требований и обязанностей.

    Attributes:
        requirement: Требования от кандидата
        responsibility: Обязанности позиции

    """

    requirement: str | None
    responsibility: str | None


class Experience(BaseModel):
    """
    Требуемый опыт.

    Attributes:
        name: Требуемый опыт

    """

    id: str
    name: str | None = None


class Vacancy(BaseModel):
    id: str
    name: str
    area: Area
    salary: Salary | None = None
    vacancy_brief: VacancyBrief | None
    experience: Experience | None = None
    employer: Employer
    published_at: datetime
    archived: bool | None = None
