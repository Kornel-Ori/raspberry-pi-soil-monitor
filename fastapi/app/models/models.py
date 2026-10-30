from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(320),
        unique=True,
        nullable=False
    )

    image_file: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
        default=None
    )

    readings: Mapped[list[Reading]] = relationship(
        back_populates="author"
    )


class Reading(Base):
    __tablename__ = "reading"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    sensor: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    content: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
        nullable=False,
        index=True
    )

    date_timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    author: Mapped[User] = relationship(
        back_populates="readings"
    )


class WateringEvent(Base):
    __tablename__ = "watering_event"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    sensor: Mapped[str] = mapped_column(
        String(50), nullable=False
    )

    date_timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    amount_ml: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )