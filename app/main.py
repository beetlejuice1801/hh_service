import logging

import uvicorn
from config.settings import settings

logging.basicConfig(
    level=settings.app.logging.level_name,
    format=settings.app.logging.format,
    datefmt=settings.app.logging.datefmt,
)


def main():
    uvicorn.run(
        "app:app",
        host=settings.app.host,
        port=settings.app.port,
        reload=True,
    )


if __name__ == "__main__":
    main()
