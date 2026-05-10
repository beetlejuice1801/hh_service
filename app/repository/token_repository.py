from datetime import datetime, timedelta
from sqlalchemy import select
from schemas.tokens import CodeResponse
from models import async_session, UserToken
from exceptions import NoTokenFound


class TokenRepository:
    def __init__(self):
        pass

    @staticmethod
    async def save_token(
        token_schema: CodeResponse,
        user_id: str,
    ):
        user_token = UserToken(
            user_id=user_id,
            access_token=token_schema.access_token.get_secret_value(),
            refresh_token=token_schema.refresh_token.get_secret_value(),
            expires_at=datetime.now()
            + timedelta(
                seconds=token_schema.expires_in,
            ),
        )

        async with async_session() as session:
            session.add(user_token)
            await session.commit()

    @staticmethod
    async def get_token(
        user_id: str,
    ):
        async with async_session() as session:
            stmt = select(UserToken).where(
                UserToken.user_id == user_id,
            )
            result = await session.scalars(stmt)
            user_token = result.first()
            if user_token is None:
                raise NoTokenFound()
            return user_token.access_token
