import logging
from typing import Literal
from pydantic import BaseModel

# Не самый удачный формат логирования, поменять
LOGGING_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


class LoggingConfig(BaseModel):
    """Настройки логирования."""

    level_name: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"
    format: str = LOGGING_FORMAT

    @property
    def level(self) -> int:
        return logging.getLevelNamesMapping()[self.level_name]


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
