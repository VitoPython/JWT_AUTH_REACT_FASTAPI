from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.model import Users  # Import the Users model
from fastapi import HTTPException  # Import HTTPException from fastapi

class UserService:

    @staticmethod
    async def get_user_profile(username: str):
        async with AsyncSession() as session:
            query = select(Users).where(Users.username == username)
            result = await session.execute(query)
            user = result.scalar_one_or_none()  # Получаем один объект или None
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            # Преобразуем SQLAlchemy объект в словарь
            return {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "person": {
                    "name": user.person.name,
                    "birth": user.person.birth,
                    "sex": user.person.sex,
                    "profile": user.person.profile
                }
            }
