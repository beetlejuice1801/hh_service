from pathlib import Path
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    PydanticBaseSettingsSource,
    YamlConfigSettingsSource,
)
from config.app import AppConfig
from config.db import DatabaseConfig

# Использую только абсолютные пути
CURRENT_DIR = Path(__file__).resolve().parent
ENVS_DIR = CURRENT_DIR / "envs"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="SERVICE_APP__",
        env_nested_delimiter="__",
        env_file=ENVS_DIR / ".env",
        case_sensitive=False,
    )
    app: AppConfig = AppConfig()
    db: DatabaseConfig

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            YamlConfigSettingsSource(
                settings_cls,
            ),
        )


settings = Settings()
