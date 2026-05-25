import logging

import aiohttp
import asyncio
import random
from repository import TokenRepository
from config.settings import settings

log = logging.getLogger(__name__)
repository = TokenRepository()


class HHVacancyCollector:
    """
    Асинхронный коллектор вакансий с HeadHunter API.

    Этот класс управляет сбором вакансий с использованием асинхронных запросов,
    контролирует конкурентность запросов и автоматически управляет HTTP-сессией.

    Атрибуты класса:
        url (str): URL эндпоинта для получения вакансий из настроек

    Атрибуты экземпляра:
        access_token (str): Токен доступа для авторизации в API HH
        semaphore (asyncio.Semaphore): Семафор для ограничения количества одновременных запросов
        session (aiohttp.ClientSession): HTTP-сессия для выполнения запросов
    """

    url = settings.app.url_for_fetch_vacancies

    def __init__(self, access_token, max_concurrency: int = 10):
        self.access_token = access_token
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def __aenter__(self):
        """
        Асинхронный вход в контекстный менеджер.

        Создает HTTP-сессию с необходимыми заголовками авторизации.
        Автоматически вызывается при использовании `async with`.

        Returns:
            HHVacancyCollector: Экземпляр самого коллектора для использования в контексте
        """
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "User-Agent": settings.app.user_agent,
            },
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Асинхронный выход из контекстного менеджера.

        Закрывает HTTP-сессию для освобождения ресурсов.
        Автоматически вызывается при выходе из блока `async with`.

        Args:
            exc_type: Тип исключения, если оно возникло
            exc_val: Значение исключения
            exc_tb: Трассировка исключения
        """
        await self.session.close()

    async def fetch_page(self, params: dict, page) -> dict:
        """
        Получение одной страницы вакансий из API HeadHunter.

        Args:
            params (Dict[str, Any]): Параметры запроса (текст, регион и т.д.)
            page (int): Номер страницы для загрузки (начиная с 0)

        Returns:
            Dict[str, Any]: JSON-ответ от API, содержащий вакансии на странице
        """
        params["page"] = page
        async with self.session.get(self.url, params=params) as response:
            return await response.json()

    async def fetch_page_safe(self, params: dict, page) -> dict:
        """
        Безопасное получение страницы вакансий с ограничением конкурентности и задержкой.

        Использует семафор для ограничения количества одновременных запросов
        и добавляет случайную задержку для соблюдения rate limiting API.

        Args:
            params (dict): Параметры запроса
            page (int): Номер страницы для загрузки

        Returns:
            JSON-ответ от API с вакансиями
        """
        async with self.semaphore:
            await asyncio.sleep(random.uniform(0.5, 3))
            return await self.fetch_page(params, page)

    async def fetch_vacancies(self, params: dict) -> list:
        """
        Получение всех вакансий по заданным параметрам.

        Этот метод определяет общее количество страниц,
        создает задачи для параллельной загрузки всех страниц,
        и объединяет результаты в один список.

        Args:
            params: Параметры поиска вакансий
                (text, area, salary и другие фильтры HH API)

        Returns:
            Список всех вакансий, собранных со всех страниц
        """
        all_vacancies = []
        fetch_page = await self.fetch_page(params, page=0)
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
