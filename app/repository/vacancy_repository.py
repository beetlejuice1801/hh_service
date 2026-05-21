from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import row

from schemas import VacancySchema, EmployerSchema
from models import async_session, Vacancy, Employer


class VacancyRepository:
    def __init__(self):
        pass

    @staticmethod
    async def update_vacancy(
        vacancy_schema: VacancySchema,
        employer_schema: EmployerSchema,
    ):
        employer_stmt = insert(Employer).values(
            id=employer_schema.id,
            name=employer_schema.name,
            url=employer_schema.url,
        )
        upsert_employer_stmt = employer_stmt.on_conflict_do_update(
            index_elements=[Employer.id],
            set_={
                "name": employer_stmt.excluded.name,
                "url": employer_stmt.excluded.url,
            },
        )
        vacancy_stmt = insert(Vacancy).values(
            id=vacancy_schema.id,
            employer_id=vacancy_schema.employer.id,
            name=vacancy_schema.name,
            area=vacancy_schema.area.name,
            salary_from=(
                vacancy_schema.salary.from_ if vacancy_schema.salary else None
            ),
            salary_to=(vacancy_schema.salary.to if vacancy_schema.salary else None),
            snippet_requirement=(
                vacancy_schema.snippet.requirement if vacancy_schema.snippet else None
            ),
            snippet_responsibility=(
                vacancy_schema.snippet.responsibility
                if vacancy_schema.snippet
                else None
            ),
            experience=(
                vacancy_schema.experience.name if vacancy_schema.experience else None
            ),
            published_at=vacancy_schema.published_at,
            raw_data=vacancy_schema.raw_data,
        )
        upsert_vacancy_stmt = vacancy_stmt.on_conflict_do_update(
            index_elements=[Vacancy.id],
            set_={
                "name": vacancy_stmt.excluded.name,
                "area": vacancy_stmt.excluded.area,
                "salary_from": vacancy_stmt.excluded.salary_from,
                "salary_to": vacancy_stmt.excluded.salary_to,
                "experience": vacancy_stmt.excluded.experience,
                "snippet_requirement": vacancy_stmt.excluded.snippet_requirement,
                "snippet_responsibility": vacancy_stmt.excluded.snippet_responsibility,
                "raw_data": vacancy_stmt.excluded.raw_data,
            },
        )

        async with async_session() as session:
            await session.execute(upsert_employer_stmt)
            await session.execute(upsert_vacancy_stmt)
            await session.commit()

    @staticmethod
    async def get_vacancies(
        salary_from: int = None,
        salary_to: int = None,
        name: str = None,
        experience: str = None,
        order_by: str = "published_at",
        order_direction: str = "desc",
    ):
        async with async_session() as session:
            stmt = select(Vacancy)
            if salary_from:
                stmt = stmt.where(Vacancy.salary_from >= salary_from)
            if salary_to:
                stmt = stmt.where(Vacancy.salary_to <= salary_to)
            if name:
                stmt = stmt.where(Vacancy.name.ilike(f"%{name}%"))
            if experience:
                stmt = stmt.where(Vacancy.experience == experience)

            column = getattr(Vacancy, order_by, Vacancy.published_at)
            if order_direction == "desc":
                stmt = stmt.order_by(column.desc())
            else:
                stmt = stmt.order_by(column.asc())

            result = await session.execute(stmt)
            return result.scalars().all()

    @staticmethod
    async def get_median_salary():
        stmt = select(
            func.percentile_cont(0.5).within_group(
                Vacancy.salary_from.asc(),
            )
        )
        async with async_session() as session:
            result = await session.execute(stmt)
            median = result.scalar()
            return median

    @staticmethod
    async def frequency_distribution():
        stmt = (
            select(Vacancy.experience, func.count().label("count"))
            .group_by(Vacancy.experience)
            .order_by(func.count().desc())
        )
        async with async_session() as session:
            result = await session.execute(stmt)
            rows = result.all()
            frequency = [(exp, count) for exp, count in rows]
            return frequency

    @staticmethod
    async def get_vacancy_by_id(id_):
        stmt = select(Vacancy).where(Vacancy.id == id_)
        async with async_session() as session:
            result = await session.execute(stmt)
            vacancy_by_id = result.scalar()
            return vacancy_by_id
