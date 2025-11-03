from datetime import datetime
import uuid
import enum

from fastapi_users import schemas


class UserRole(enum.Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"


class UserRead(schemas.BaseUser[uuid.UUID]):
    first_name: str
    last_name: str
    role: UserRole

class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    role: UserRole

class UserUpdate(schemas.BaseUserUpdate):
    pass

