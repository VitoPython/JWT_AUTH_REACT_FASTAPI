from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi.security import HTTPAuthorizationCredentials
from app.config import get_session
from app.repository.auth_repo import JWTBearer, JWTRepo
from app.model import Users

router = APIRouter()

@router.get("/users/", dependencies=[Depends(JWTBearer())])
async def get_user_profile(
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer()),
    db: AsyncSession = Depends(get_session)
):
    
    token_data = JWTRepo.extract_token(credentials)
    username = token_data["username"]

    
    query = select(Users).options(selectinload(Users.person)).where(Users.username == username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    
    return {
        "detail": "Successfully fetched data!",
        "result": {
            "username": user.username,
            "email": user.email,
            "phone_number": user.person.phone_number,
            "name": user.person.name,
            "birth": user.person.birth.strftime("%Y-%m-%d"),
            "sex": user.person.sex,
            "profile": user.person.profile,
        },
    }
