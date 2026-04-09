from pydantic import BaseModel, SecretStr
from sqlalchemy import URL


class SqlaConfig(BaseModel):
    max_overflow: int = 10
    driver: str = "postgresql+asyncpg"
    pool_size: int = 100
    echo: bool = False


class DatabaseConfig(BaseModel):
    host: str
    port: int = 5432
    user: str
    password: SecretStr
    database: str

    sqla: SqlaConfig = SqlaConfig()

    @property
    def async_url(self) -> URL:
        return URL.create(
            host=self.postgres.host,
            port=self.postgres.port,
            drivername=self.postgres.driver,
            username=self.postgres.user,
            password=self.postgres.password.get_secret_value(),
            database=self.postgres.database,
        )
