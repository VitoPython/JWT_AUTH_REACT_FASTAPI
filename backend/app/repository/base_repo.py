from typing import Generic, TypeVar, Type, List
from sqlalchemy import update as sql_update, delete as sql_delete
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import get_session

T = TypeVar("T")


class BaseRepo(Generic[T]):
    model: Type[T] = None

    @classmethod
    async def create(cls, **kwargs) -> T:
        async for session in get_session():  # Используем контекстный менеджер сессий
            model = cls.model(**kwargs)
            session.add(model)
            await session.commit()
            return model

    @classmethod
    async def get_all(cls) -> List[T]:
        async for session in get_session():
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_by_id(cls, model_id: str) -> T:
        async for session in get_session():
            query = select(cls.model).where(cls.model.id == model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def update(cls, model_id: str, **kwargs):
        async for session in get_session():
            query = (
                sql_update(cls.model)
                .where(cls.model.id == model_id)
                .values(**kwargs)
                .execution_options(synchronize_session="fetch")
            )
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete(cls, model_id: str):
        async for session in get_session():
            query = sql_delete(cls.model).where(cls.model.id == model_id)
            await session.execute(query)
            await session.commit()
