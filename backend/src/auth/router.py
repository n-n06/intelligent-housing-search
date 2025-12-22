from fastapi import APIRouter, Depends, Response
from fastapi_users import fastapi_users
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.strategy import get_jwt_strategy
from src.auth.models import User
from src.auth.strategy import fastapi_users, auth_backend
from src.auth.schemas import UserCreate, UserRead, UserUpdate
from src.auth.dependencies import current_active_user
from src.db import get_db

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend)
)
auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)
auth_router.include_router(
    fastapi_users.get_reset_password_router(),
)
auth_router.include_router(
    fastapi_users.get_verify_router(UserRead),
)
auth_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
)

