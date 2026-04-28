import aiohttp


class HHVacancyCollector:
    url = "https://api.hh.ru/vacancies/"

    def __init__(self):
        pass

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    def fetch_vacancies(self):
        pass
