from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

from api import router as api_router
from exceptions import NoTokenFound

app = FastAPI()

app.include_router(api_router)


@app.exception_handler(NoTokenFound)
async def token_not_found(request: Request, exc: NoTokenFound):
    return RedirectResponse(url="/auth/login")
