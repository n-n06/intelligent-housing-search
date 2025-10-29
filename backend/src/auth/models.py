import uuid
from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import TIMESTAMP, String
from sqlalchemy.orm import Mapped, MappedColumn, mapped_column

from src.db import Base

class User(SQLAlchemyBaseUserTable[uuid.UUID], Base):
    __tablename__ = "users"

    user_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    firstname: Mapped[str] = mapped_column(String(255), nullable=False)
    lastname: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(1024), nullable=False)
    role: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=False))
