from typing import Literal
from pydantic import BaseModel, SecretStr
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
    client_id: SecretStr = str
    client_secret: SecretStr = str
    user_id: SecretStr = str
    redirect_uri: str = "http://localhost:8080/auth/callback"
    user_agent: str = "hh-service/1.0 (longineslacatedral@gmail.com)"
    current_user: str = "https://api.hh.ru/me"
    get_token_url: str = "https://api.hh.ru/token"
