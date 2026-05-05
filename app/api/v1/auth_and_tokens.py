from fastapi import APIRouter, status
from models import Vacancy, Employer
from requests import Request
from fastapi.responses import RedirectResponse
from config.settings import settings

router = APIRouter(prefix="/login")


@router.get("/")
async def auth():
    pass


@router.get("/refresh_token")
async def refresh_token():
    pass
