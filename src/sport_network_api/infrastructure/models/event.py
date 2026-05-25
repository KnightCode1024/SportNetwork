from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Table, Column, String, Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sport_network_api.infrastructure.models import Base

if TYPE_CHECKING:
    from sport_network_api.infrastructure.models.user import User


event_participants = Table(
    "event_participants",
    Base.metadata,
    Column("event_id", ForeignKey("events.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)


class Event(Base):
    __tablename__ = "events"

    title: Mapped[str] = mapped_column(
        String(),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        Text(),
        nullable=True,
    )
    address: Mapped[str] = mapped_column(
        String(),
        nullable=False,
    )
    sport_type: Mapped[str] = mapped_column(
        String(),
        nullable=False,
    )
    organizer_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    max_participants: Mapped[int] = mapped_column(
        Integer(),
        nullable=False,
        default=1,
    )

    organizer: Mapped[User] = relationship(
        "User",
        lazy="joined",
    )
    participants: Mapped[list[User]] = relationship(
        "User",
        secondary=event_participants,
        lazy="selectin",
    )
