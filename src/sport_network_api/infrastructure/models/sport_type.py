from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sport_network_api.infrastructure.models import Base

if TYPE_CHECKING:
    from sport_network_api.infrastructure.models.event import Event


class SportType(Base):
    __tablename__ = "sport_types"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(
        String(),
        nullable=False,
        unique=True,
    )
    description: Mapped[str] = mapped_column(
        String(),
        nullable=True,
    )
    events: Mapped[list[Event]] = relationship(
        "Event",
        back_populates="sport_type",
    )