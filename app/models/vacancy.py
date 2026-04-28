from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    Integer,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.dialects.postgresql import JSONB
from models.base import Base

if TYPE_CHECKING:
    from models.employer import Employer


class Vacancy(Base):
    __tablename__ = "vacancies"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    employer_id: Mapped[str] = mapped_column(ForeignKey("employers.id"))
    name: Mapped[str] = mapped_column(String)
    area: Mapped[str] = mapped_column(String)
    salary_from: Mapped[int | None] = mapped_column(Integer)
    salary_to: Mapped[int | None] = mapped_column(Integer)
    experience: Mapped[str] = mapped_column(String)
    work_format: Mapped[str] = mapped_column(String)
    published_at: Mapped[datetime] = mapped_column(DateTime)
    raw_data: Mapped[dict] = mapped_column(JSONB)
    first_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now,
    )
    last_updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now,
        onupdate=datetime.now,
    )

    employer: Mapped["Employer"] = relationship(
        back_populates="vacancies",
    )
    skills: Mapped[list["VacancySkill"]] = relationship(
        back_populates="vacancy",
    )


class VacancySkill(Base):
    __tablename__ = "vacancy_skills"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    vacancy_id: Mapped[str] = mapped_column(ForeignKey("vacancies.id"))
    skill_name: Mapped[str] = mapped_column(String, nullable=False)

    vacancy: Mapped["Vacancy"] = relationship(back_populates="skills")
