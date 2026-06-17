from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    PASSENGER = "passenger"
    DRIVER = "driver"


class VehicleStatus(str, Enum):
    AVAILABLE = "available"
    IN_USE = "in_use"
    MAINTENANCE = "maintenance"


class TripStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_TRANSIT = "in_transit"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"