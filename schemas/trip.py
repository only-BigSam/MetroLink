from datetime import datetime

from pydantic import BaseModel, ConfigDict

from models.enums import TripStatus


class TripCreate(BaseModel):
    route_id: int
    vehicle_id: int
    driver_id: int
    departure_time: datetime
    arrival_time: datetime


class TripResponse(BaseModel):
    id: int
    route_id: int
    vehicle_id: int
    driver_id: int
    departure_time: datetime
    arrival_time: datetime
    status: TripStatus

    class Config:
        from_attributes = True

class TripStatusUpdate(BaseModel):
    status: TripStatus

class DriverTripResponse(BaseModel):
    trip_id: int
    route_name: str
    departure_time: datetime
    arrival_time: datetime
    vehicle_number: str
    trip_status: TripStatus

    model_config = ConfigDict(from_attributes=True)

class AdminTripResponse(BaseModel):
    id: int
    route: str
    driver: str
    vehicle: str
    departure_time: datetime
    arrival_time: datetime
    status: TripStatus

    model_config = ConfigDict(from_attributes=True)

class TripStatisticsResponse(BaseModel):
    trip_id: int
    trip_status: TripStatus
    vehicle_capacity: int
    booked_seats: int
    available_seats: int
    total_bookings: int