from __future__ import annotations

from typing import TYPE_CHECKING
from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey, Enum as SQLEnum, Date

from sport_network_api.infrastructure.models import Base
from sport_network_api.domain.enums import Gender

if TYPE_CHECKING:
    from sport_network_api.infrastructure.models import User


class Profile(Base):
    __tablename__ = "profiles"

    bio: Mapped[str] = mapped_column(
        Text(),
        nullable=True,
    )
    avatar_url: Mapped[str] = mapped_column(
        String(),
        nullable=True,
    )
    date_of_birth: Mapped[date] = mapped_column(
        Date(),
        nullable=True,
    )
    gender: Mapped[Gender] = mapped_column(
        SQLEnum(Gender),
        nullable=True,
        default=None,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
    )
    user: Mapped[User] = relationship(
        back_populates="profile",
    )
