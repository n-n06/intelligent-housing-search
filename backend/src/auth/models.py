from datetime import datetime
import uuid

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import TIMESTAMP, String, func, Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base
from src.auth.schemas import UserRole

class User(SQLAlchemyBaseUserTable[uuid.UUID], Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(1024), nullable=False)
    role: Mapped[str] = mapped_column(
        Enum(UserRole), nullable=False, default=UserRole.CUSTOMER
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False), 
        server_default=func.now(),
        nullable=False
    )
