from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)
from config.settings import settings

engine = create_engine(
    url=settings.db.url,
    echo=settings.db.sqla.echo,
    pool_size=settings.db.sqla.pool_size,
    max_overflow=settings.db.sqla.max_overflow,
)

async_engine = create_async_engine(
    url=settings.db.async_url,
    echo=settings.db.sqla.echo,
    pool_size=settings.db.sqla.pool_size,
    max_overflow=settings.db.sqla.max_overflow,
)

async_session = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)
