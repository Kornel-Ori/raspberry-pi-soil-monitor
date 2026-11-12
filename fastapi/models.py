from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True)

    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False)

    email: Mapped[str] = mapped_column(
        String(320), unique=True, nullable=False)

    password_hash: Mapped[str] = mapped_column(
        String(255), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    
    role: Mapped[str] = mapped_column(
        String(20),nullable=False, default="user")

    plants: Mapped[list[Plant]] = relationship(
        back_populates="user", cascade="all, delete-orphan")


class PlantSpecies(Base):
    __tablename__ = "plant_species"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True)

    common_name: Mapped[str] = mapped_column(
        String(100), nullable=False)

    botanical_name: Mapped[str|None] = mapped_column(
        String(100), nullable=True)

    description: Mapped[str|None] = mapped_column(
        Text, nullable=True)

    min_moisture: Mapped[float] = mapped_column(
        Float, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    plants: Mapped[list[Plant]] = relationship(
        back_populates="species")


class Plant(Base):
    __tablename__ = "plant"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False, index=True)

    species_id: Mapped[int] = mapped_column(
        ForeignKey("plant_species.id"), nullable=False, index=True)
    
    plant_name: Mapped[str] = mapped_column(
        String(100), nullable=False)

    location: Mapped[str|None] = mapped_column(
        String(100), nullable=True)

    min_moisture: Mapped[float|None] = mapped_column(
        Float, nullable=True)

    image_url: Mapped[str | None] = mapped_column(
        String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    
    user: Mapped[User] = relationship(
        back_populates="plants")

    species: Mapped[PlantSpecies] = relationship(
        back_populates="plants")

    alerts: Mapped[list[Alert]] = relationship(
        back_populates="plant")

    nodes: Mapped[list[Node]] = relationship(
        back_populates="plant")


class Node(Base):
    __tablename__ = "node"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True)

    device_name: Mapped[str] = mapped_column(
        String(100), nullable=False)

    status: Mapped[str] = mapped_column(
        String(20), default="offline")

    led_status: Mapped[str] = mapped_column(
        String(20), default="off")

    last_seen: Mapped[datetime|None] = mapped_column(
        DateTime(timezone=True), nullable=True)

    plant_id: Mapped[int] = mapped_column(
        ForeignKey("plant.id"), nullable=False, index=True)

    plant: Mapped[Plant] = relationship(
        back_populates="nodes")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),nullable=False, default=lambda: datetime.now(timezone.utc))

    readings: Mapped[list[Reading]] = relationship(
        back_populates="node")


class Reading(Base):
    __tablename__ = "reading"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True)

    moisture_percent: Mapped[float] = mapped_column(
        Float, nullable=False)

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    node_id: Mapped[int] = mapped_column(
        ForeignKey("node.id"), nullable=False, index=True)

    node: Mapped[Node] = relationship(
        back_populates="readings")

    alerts: Mapped[list[Alert]] = relationship(
        back_populates="reading")


class Alert(Base):
    __tablename__ = "alert"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True)

    message: Mapped[str] = mapped_column(
        String(500), nullable=False)

    status: Mapped[str] = mapped_column(
        String(20), default="active")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    plant_id: Mapped[int] = mapped_column(
        ForeignKey("plant.id"), nullable=False, index=True)

    reading_id: Mapped[int|None] = mapped_column(
        ForeignKey("reading.id"), nullable=True, index=True)

    resolved_at: Mapped[datetime|None] = mapped_column(
        DateTime(timezone=True), nullable=True)

    plant: Mapped[Plant] = relationship(
        back_populates="alerts")

    reading: Mapped[Reading|None] = relationship(
        back_populates="alerts")