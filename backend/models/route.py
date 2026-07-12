from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class Route(Base):
    __tablename__ = "routes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    origin: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    destination: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    distance: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    fare: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    trips = relationship("Trip",back_populates="route")