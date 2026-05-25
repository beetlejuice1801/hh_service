from datetime import datetime, timedelta
from typing import Literal
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from schemas.tokens import CodeResponse
from models import async_session, UserToken
from exceptions import NoTokenFound


class TokenRepository:
    """Репозиторий для работы с токенами пользователя в БД."""

    def __init__(self):
        pass

    @staticmethod
    async def save_token(
        token_schema: CodeResponse,
        user_id: str,
    ):
        """Сохраняет или обновляет токены пользователя (UPSERT)."""
        user_token_stmt = insert(UserToken).values(
            user_id=user_id,
            access_token=token_schema.access_token.get_secret_value(),
            refresh_token=token_schema.refresh_token.get_secret_value(),
            expires_at=datetime.now()
            + timedelta(
                seconds=token_schema.expires_in,
            ),
        )
        upsert_user_token_stmt = user_token_stmt.on_conflict_do_update(
            index_elements=[UserToken.user_id],
            set_={"user_id": user_token_stmt.excluded.user_id},
        )

        async with async_session() as session:
            await session.execute(upsert_user_token_stmt)
            await session.commit()

    @staticmethod
    async def get_token(
        user_id: str, token_type: Literal["access_token", "refresh_token"]
    ) -> str:
        """Получает токен пользователя по его ID и типу."""
        async with async_session() as session:
            stmt = select(UserToken).where(
                UserToken.user_id == user_id,
            )
            result = await session.scalars(stmt)
            user_token = result.one_or_none()
            if user_token is None:
                raise NoTokenFound()
            return getattr(user_token, token_type)

    @staticmethod
    async def update_token(
        token_schema: CodeResponse,
        user_id: str,
    ) -> None:
        """Обновляет существующие токены пользователя."""
        async with async_session() as session:
            stmt = (
                update(UserToken)
                .where(UserToken.user_id == user_id)
                .values(
                    user_id=user_id,
                    access_token=token_schema.access_token.get_secret_value(),
                    refresh_token=token_schema.refresh_token.get_secret_value(),
                    expires_at=datetime.now()
                    + timedelta(
                        seconds=token_schema.expires_in,
                    ),
                )
            )
            await session.execute(stmt)
            await session.commit()
