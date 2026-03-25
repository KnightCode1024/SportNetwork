from typing import TYPE_CHECKING

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Boolean

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
    is_active: Mapped[bool] = mapped_column(
        Boolean(),
        default=False,
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
