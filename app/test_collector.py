import asyncio
from collectors.vacancy_collector import HHVacancyCollector


async def main():
    async with HHVacancyCollector() as collector:
        vacancies = await collector.fetch_vacancies({})
        print(len(vacancies))
        print(vacancies[0])


if __name__ == "__main__":
    asyncio.run(main())
