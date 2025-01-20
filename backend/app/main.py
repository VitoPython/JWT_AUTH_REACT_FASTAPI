import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import init_db, engine
from app.service.auth_service import generate_roles
origins= [
    "http://localhost:3000"
]
def init_app():
    app = FastAPI(
        title="Vitalii App",
        description="Login and Sign In Authentication System",
        version="1",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    # События приложения
    @app.on_event("startup")
    async def startup():
        # Генерация ролей и создание таблиц
        await init_db()
        await generate_roles()

    @app.on_event("shutdown")
    async def shutdown():
        await engine.dispose()

    # Подключение роутеров
    from app.controller import authentication, users

    app.include_router(authentication.router)
    app.include_router(users.router)

    return app


app = init_app()

def start():
    """Launched with 'poetry run start' at root level """
    uvicorn.run("app.main:app", host="localhost", port=8888, reload=True)