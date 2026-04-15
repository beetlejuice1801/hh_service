from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from models.base import Base

if TYPE_CHECKING:
    from models.vacancy import Vacancy


class Employer(Base):
    __tablename__ = "employers"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str | None] = mapped_column(String)
    vacancies: Mapped[list["Vacancy"]] = relationship(
        back_populates="employer",
    )
