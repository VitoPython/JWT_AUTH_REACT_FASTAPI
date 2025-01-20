from typing import List
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import get_session
from app.model.role import Role
from app.repository.base_repo import BaseRepo


class RoleRepository(BaseRepo):
    model = Role

    @staticmethod
    async def find_by_role_name(role_name: str) -> Role:
        async for session in get_session():
            query = select(Role).where(Role.role_name == role_name)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @staticmethod
    async def find_by_list_role_name(role_names: List[str]) -> List[Role]:
        async for session in get_session():
            query = select(Role).where(Role.role_name.in_(role_names))
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def create_list(role_names: List[Role]):
        async for session in get_session():
            session.add_all(role_names)