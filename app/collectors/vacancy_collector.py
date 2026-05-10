import aiohttp
import asyncio
import random
from repository import TokenRepository

repository = TokenRepository()


class HHVacancyCollector:
    url = "https://api.hh.ru/vacancies/"

    def __init__(self, access_token):
        self.access_token = access_token

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={
                "User-Agent": "hh-service/1.0 (longineslacatedral@gmail.com)",
                "Authorization": f"Bearer {self.access_token}",
            },
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def fetch_vacancies(self, params: dict) -> list:
        all_vacancies = []
        page = 0

        while True:
            params["page"] = page

            async with self.session.get(self.url, params=params) as response:
                response = await response.json()
                all_vacancies.extend(response["items"])

                if page >= response["pages"]:
                    break
                page += 1
                await asyncio.sleep(random.uniform(1.0, 3.0))

        return all_vacancies
