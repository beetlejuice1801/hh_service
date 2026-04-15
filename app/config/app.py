from typing import Literal
from pydantic import BaseModel
from config.configure_logging import LoggingConfig


class AppConfig(BaseModel):
    """
    Настройки приложения.

    Attributes:
        host: Хост приложения
        port: Порт приложения
        environment: Среда запуска. Влияет на уровень логирования
            и поведение отладчика
        logging: Настройки логирования.


    """

    host: str = "localhost"
    port: int = 8080

    environment: Literal[
        "development",
        "production",
        "testing",
    ] = "development"

    logging: LoggingConfig = LoggingConfig()
