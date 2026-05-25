from pydantic import BaseModel, SecretStr
from sqlalchemy import URL


class PostgresConfig(BaseModel):
    """Конфигурация подключения к PostgreSQL."""

    host: str
    port: int = 5432
    user: str
    password: SecretStr
    database: str


class SqlaConfig(BaseModel):
    """Конфигурация SQLAlchemy для работы с БД."""

    max_overflow: int = 10
    async_driver: str = "postgresql+asyncpg"
    driver: str = "postgresql+psycopg2"
    pool_size: int = 100
    echo: bool = False


class DatabaseConfig(BaseModel):
    """Общая конфигурация базы данных, объединяющая PostgresConfig и SqlaConfig."""

    postgres: PostgresConfig
    sqla: SqlaConfig = SqlaConfig()

    @property
    def async_url(self) -> URL:
        """Формирует URL для асинхронного подключения к БД через asyncpg."""
        return URL.create(
            host=self.postgres.host,
            port=self.postgres.port,
            drivername=self.sqla.async_driver,
            username=self.postgres.user,
            password=self.postgres.password.get_secret_value(),
            database=self.postgres.database,
        )

    @property
    def url(self) -> URL:
        """Формирует URL для синхронного подключения к БД через psycopg2."""
        return URL.create(
            host=self.postgres.host,
            port=self.postgres.port,
            drivername=self.sqla.driver,
            username=self.postgres.user,
            password=self.postgres.password.get_secret_value(),
            database=self.postgres.database,
        )
