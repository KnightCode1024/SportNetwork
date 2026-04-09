from enum import Enum
from typing import TYPE_CHECKING


from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Boolean, Integer, ForeignKey, Enum as SQLEnum

from sport_network_api.infrastructure.models import Base

if TYPE_CHECKING:
    from sport_network_api.infrastructure.models import User


class NotificationProviderEnum(Enum):
    EMAIL = "email"
    TELEGRAM = "telegram"
    NONE = "none"


class AccountSetting(Base):
    __tablename__ = "account_settings"

    id: Mapped[int] = mapped_column(
        Integer(),
        primary_key=True,
        autoincrement=True,
    )
    auth_2fa: Mapped[bool] = mapped_column(
        Boolean(),
        default=False,
    )
    notification_provider: Mapped[NotificationProviderEnum] = mapped_column(
        SQLEnum(NotificationProviderEnum),
        default=NotificationProviderEnum.EMAIL,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
    )
    user: Mapped[User] = relationship(
        back_populates="account_settings",
    )
