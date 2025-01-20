from typing import Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update as sql_update
from app.config import get_session
from app.model.users import Users
from app.repository.base_repo import BaseRepo


class UsersRepository(BaseRepo):
    model = Users

    @staticmethod
    async def find_by_username(username: str) -> Optional[Users]:
        async for session in get_session():  # Используем get_session для получения сессии
            query = select(Users).where(Users.username == username)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @staticmethod
    async def find_by_email(email: str) -> Optional[Users]:
        async for session in get_session():  # Используем get_session для получения сессии
            query = select(Users).where(Users.email == email)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @staticmethod
    async def update_password(email: str, password: str):
        async for session in get_session():  # Используем get_session для получения сессии
            query = (
                sql_update(Users)
                .where(Users.email == email)
                .values(password=password)
                .execution_options(synchronize_session="fetch")
            )
            await session.execute(query)
            await session.commit()
