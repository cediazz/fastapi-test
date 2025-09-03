from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .. import models
from ..schemas import user_schemas
from ..auth import get_password_hash
from fastapi import HTTPException, status, Depends
from ..auth import oauth2_scheme, verify_password, create_access_token
from ..database import get_async_session
from jose import JWTError, jwt
from ..config import get_settings
from ..schemas.user_schemas import TokenData
from datetime import timedelta

class UserService:
    
    
    async def get_user_by_email(self,session: AsyncSession, email: str):
        result = await session.execute(
        select(models.User).where(models.User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_user_by_id(self, session: AsyncSession, user_id: int):
        result = await session.execute(
        select(models.User).where(models.User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def create_user(self, session: AsyncSession, user: user_schemas.UserCreate):
        db_user = await self.get_user_by_email(session, user.email)
        if db_user:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already registered"
        )
        hashed_password = get_password_hash(user.password)
        db_user = models.User(
            email=user.email,
            hashed_password=hashed_password,
            full_name=user.full_name
            )
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user
    
    async def login(
        self,
        email: str,
        password: str,
        session: AsyncSession
    ):
        user = await self.get_user_by_email(session, email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES)
            )
        return {"access_token": access_token, "token_type": "bearer"}