from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class Driver(Base):
    __tablename__ = "drivers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    license_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    phone_number: Mapped[str] = mapped_column(
        String(20),
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
    

    user = relationship("User", back_populates="driver")

    trips = relationship("Trip",back_populates="driver")