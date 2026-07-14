from sqlalchemy import ForeignKey, String, Integer, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional

from app.database import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)

class Site(Base):
    __tablename__ = 'sites'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    url: Mapped[str]
    name: Mapped[str]
    status_code: Mapped[Optional[int]] = mapped_column(nullable=True)
    is_online: Mapped[bool] = mapped_column(default=True)
    last_checked: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))