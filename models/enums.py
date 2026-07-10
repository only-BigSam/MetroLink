from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    PASSENGER = "PASSENGER"
    DRIVER = "DRIVER"


class VehicleStatus(str, Enum):
    AVAILABLE = "available"
    IN_USE = "in_use"
    MAINTENANCE = "maintenance"


class TripStatus(str, Enum):
    SCHEDULED = "SCHEDULED"
    IN_TRANSIT = "IN_TRANSIT"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class BookingStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"