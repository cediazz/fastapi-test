from fastapi import APIRouter,Depends
from ..schemas import user_schemas
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_async_session
from ..services.user_services import UserService

users_routers = APIRouter(
    prefix="/users",
    tags=["users"],
)

@users_routers.post("/register", response_model=user_schemas.UserResponse)
async def register_user(user: user_schemas.UserCreate, session: AsyncSession = Depends(get_async_session)):
    return await UserService().create_user(session, user)

@users_routers.post("/login", response_model=user_schemas.Token)
async def login(
    email: str,
    password: str,
    session: AsyncSession = Depends(get_async_session)
):
    return await UserService().login(email,password,session)