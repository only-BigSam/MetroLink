from datetime import datetime

from pydantic import BaseModel

from models.enums import BookingStatus, TripStatus


class BookingCreate(BaseModel):
    trip_id: int
    seats_booked: int


class BookingResponse(BaseModel):
    id: int
    trip_id: int
    seats_booked: int
    status: BookingStatus

    class Config:
        from_attributes = True

class BookingDetailedResponse(BaseModel):
    id: int
    trip_id: int
    seats_booked: int
    status: BookingStatus

    departure_time: datetime
    arrival_time: datetime
    route_name: str
    vehicle_number: str
    trip_status: TripStatus

    class Config:
        from_attributes = True


class BookingStatusUpdate(BaseModel):
    status: BookingStatus