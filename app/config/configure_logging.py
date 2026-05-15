import logging
from typing import Literal
from pydantic import BaseModel

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOGGING_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


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
    datefmt: str = DATE_FORMAT

    @property
    def level(self) -> int:
        return logging.getLevelNamesMapping()[self.level_name]
