from fastapi import APIRouter, HTTPException
import aiohttp
from yarl import URL
from fastapi.responses import RedirectResponse
from config.settings import settings
from repository import TokenRepository
from schemas.tokens import CodeResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login")
async def auth() -> RedirectResponse:
    """
    Эндпоинт для инициации процесса аутентификации через HeadHunter.

    Формирует URL для редиректа на страницу авторизации HH.ru с необходимыми параметрами.
    Пользователь перенаправляется на страницу входа HH, где вводит свои учетные данные.

    Returns:
        RedirectResponse: Объект редиректа на страницу авторизации HH.ru
    """
    params = {
        "response_type": "code",
        "client_id": settings.app.client_id.get_secret_value(),
        "redirect_uri": settings.app.redirect_uri,
    }
    url = URL("https://hh.ru/oauth/authorize").with_query(params)
    return RedirectResponse(url=url)


@router.get("/callback")
async def callback(code: str):
    """
    Callback эндпоинт, который обрабатывает ответ от HeadHunter после авторизации.

    Получает авторизационный код, обменивает его на токены доступа,
    получает информацию о пользователе и сохраняет токены в БД.

    Args:
        code (str): Авторизационный код, переданный от HH.ru после успешного входа

    Returns:
        Словарь с сообщением об успешном сохранении токена

    Raises:
        HTTPException: Если HH вернул ошибку в ответе
    """
    url = settings.app.get_token_url
    params = {
        "client_id": settings.app.client_id.get_secret_value(),
        "client_secret": settings.app.client_secret.get_secret_value(),
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": settings.app.redirect_uri,
    }
    async with aiohttp.ClientSession(
        headers={
            "User-Agent": settings.app.user_agent,
        }
    ) as session:
        async with session.post(url=url, data=params) as response:
            response_data = await response.json()
            if "error" in response_data:
                raise HTTPException(status_code=400, detail=response_data["error"])
            token_data = CodeResponse(**response_data)
        async with session.get(
            url=settings.app.current_user,
            headers={
                "Authorization": f"Bearer {token_data.access_token.get_secret_value()}"
            },
        ) as response:
            response_data = await response.json()
            user_id = response_data["id"]
            repo = TokenRepository()
            await repo.save_token(token_data, user_id=user_id)
    return {"message": "Токен успешно сохранён!"}


@router.get("/refresh_token")
async def refresh_token():
    """
    Эндпоинт для обновления истекшего access токена.

    Использует refresh token для получения новой пары токенов доступа.
    Обновляет токены в базе данных.

    Returns:
        Словарь с сообщением об успешном обновлении токена

    Raises:
        HTTPException: Если HH вернул ошибку при обновлении токена
    """
    url = settings.app.get_token_url
    token = (
        await TokenRepository.get_token(
            user_id=settings.app.user_id.get_secret_value(),
            token_type="refresh_token",
        ),
    )

    params = {"grant_type": "refresh_token", "refresh_token": token}
    async with aiohttp.ClientSession(
        headers={"User-Agent": settings.app.user_agent}
    ) as session:
        async with session.post(url=url, data=params) as response:
            response_data = await response.json()
            if "error" in response_data:
                raise HTTPException(status_code=400, detail=response_data["error"])
            token_data = CodeResponse(**response_data)
            repo = TokenRepository()
            await repo.update_token(
                token_data,
                user_id=settings.app.user_id.get_secret_value(),
            )
            return {"message": "Токен успешно обновлён"}
