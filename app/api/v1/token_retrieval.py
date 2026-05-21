import logging

from fastapi import APIRouter, HTTPException
from sqlalchemy import URL
import aiohttp
from yarl import URL
from fastapi.responses import RedirectResponse
from config.settings import settings
from repository import TokenRepository
from schemas.tokens import CodeResponse
from models import UserToken

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login")
async def auth() -> RedirectResponse:
    params = {
        "response_type": "code",
        "client_id": settings.app.client_id.get_secret_value(),
        "redirect_uri": settings.app.redirect_uri,
    }
    url = URL("https://hh.ru/oauth/authorize").with_query(params)
    return RedirectResponse(url=url)


@router.get("/callback")
async def callback(code: str):
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
    return RedirectResponse(url="http://localhost:8080/auth/me")


@router.get("/me")
async def me():
    return {"message": "Успешно!"}


@router.get("/refresh_token")
async def refresh_token():
    url = settings.app.get_token_url
    params = {
        "grant_type": "refresh_token",
        "refresh_token": UserToken.refresh_token.get_secret_value(),
    }
    async with aiohttp.ClientSession(
        headers={"User-Agent": settings.app.user_agent},
    ) as session:
        async with session.post(url=url, data=params) as response:
            response_data = await response.json()
            if "error" in response_data:
                raise HTTPException(status_code=400, detail=response_data["error"])
            token_data = CodeResponse(**response_data)
