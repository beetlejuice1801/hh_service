import aiohttp


class HHVacancyCollector:
    url = "https://api.hh.ru/vacancies/"

    def __init__(self):
        pass

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={
                "User-Agent": "hh-service/1.0 (longineslacatedral@gmail.com)",
            },
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def fetch_vacancies(self, params: dict) -> list:
        params = {
            "text": "менеджер по продажам",
            "area": 1,
            "per_page": 30,
            "page": 0,
            "order_by": "expiration_date_asc",
        }

        async with self.session.get(self.url, params=params) as response:
            print(response.status)
            response = await response.json()
            print(response)
            return response["items"]
