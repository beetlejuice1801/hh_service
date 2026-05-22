import logging

import aiohttp
import asyncio
import random
from repository import TokenRepository
from config.settings import settings

log = logging.getLogger(__name__)
repository = TokenRepository()


class HHVacancyCollector:
    url = settings.app.url_for_fetch_vacancies

    def __init__(self, access_token, max_concurrency: int = 10):
        self.access_token = access_token
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "User-Agent": settings.app.user_agent,
            },
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def fetch_page(self, params: dict, page) -> dict:
        params["page"] = page
        async with self.session.get(self.url, params=params) as response:
            return await response.json()

    async def fetch_page_safe(self, params: dict, page) -> dict:
        async with self.semaphore:
            await asyncio.sleep(random.uniform(0.5, 3))
            return await self.fetch_page(params, page)

    async def fetch_vacancies(self, params: dict) -> list:
        all_vacancies = []
        fetch_page = await self.fetch_page(params, page=0)
        print(fetch_page)
        total_pages = fetch_page["pages"]
        tasks = [
            self.fetch_page_safe(
                params,
                page=p,
            )
            for p in range(total_pages)
        ]
        results = await asyncio.gather(*tasks)
        for result in results:
            all_vacancies.extend(result["items"])
        return all_vacancies
