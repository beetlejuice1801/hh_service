from pydantic import BaseModel, Field
from datetime import datetime


class Salary(BaseModel):
    from_: int | None = Field(
        None,
        alias="from",
    )
    to: int | None = None
    currency: str | None = None
    gross: bool | None = None


class Employer(BaseModel):
    id: str
    name: str
    url: str | None = None
    alternate_url: str | None = None
    trusted: bool


class Area(BaseModel):
    id: str
    name: str
    url: str | None = None


class Snippet(BaseModel):
    requirement: str | None
    responsibility: str | None


class Experience(BaseModel):
    id: str
    name: str | None = None


class Vacancy(BaseModel):
    id: str
    name: str
    area: Area
    salary: Salary | None = None
    snippet: Snippet | None
    experience: Experience | None = None
    employer: Employer
    published_at: datetime
    archived: bool | None = None
