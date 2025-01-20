from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

# Конфигурация базы данных
DB_CONFIG = "postgresql+asyncpg://postgres:admin@localhost:5432/postgres"
SECRET_KEY = "lemoncode21"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Создание движка
engine = create_async_engine(DB_CONFIG, future=True, echo=True)

# Фабрика для создания сессий
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Функция для создания всех таблиц
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


# Контекстный менеджер для сессий
async def get_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
