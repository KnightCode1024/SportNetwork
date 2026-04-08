from uuid import uuid4
from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Boolean, UUID, DateTime

from sport_network_api.infrastructure.models import Base


if TYPE_CHECKING:
    from sport_network_api.infrastructure.models import Profile, AccountSetting


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(),
        unique=True,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(),
        unique=True,
        nullable=False,
    )
    password: Mapped[str] = mapped_column(
        String(),
        nullable=False,
    )
    token: Mapped[UUID] = mapped_column(
        UUID(),
        unique=True,
        nullable=False,
        default=uuid4,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean(),
        default=False,
    )
    reset_token: Mapped[str | None] = mapped_column(
        String(),
        nullable=True,
        default=None,
    )
    reset_token_expires: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )

    profile: Mapped[Profile] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    account_settings: Mapped[AccountSetting] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
