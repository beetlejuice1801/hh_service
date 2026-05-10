from sqlalchemy.dialects.postgresql import insert
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
            area=vacancy_schema.area,
            salary_from=vacancy_schema.salary.from_,
            salary_to=vacancy_schema.salary.to,
            experience=vacancy_schema.experience,
            work_format=vacancy_schema.work_format,
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
                "work_format": vacancy_stmt.excluded.work_format,
                "raw_data": vacancy_stmt.excluded.raw_data,
            },
        )

        async with async_session() as session:
            await session.execute(upsert_employer_stmt)
            await session.execute(upsert_vacancy_stmt)
            await session.commit()
