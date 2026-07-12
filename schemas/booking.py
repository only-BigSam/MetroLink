from datetime import datetime

from pydantic import BaseModel, ConfigDict

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

class DriverPassengerResponse(BaseModel):
    booking_id: int
    passenger_name: str
    passenger_email: str
    seats_booked: int
    booking_status: BookingStatus

    model_config = ConfigDict(from_attributes=True)

from pydantic import BaseModel, ConfigDict

class TripPassengerResponse(BaseModel):
    booking_id: int
    passenger_name: str
    passenger_email: str
    seats_booked: int

    model_config = ConfigDict(from_attributes=True)

class AdminBookingResponse(BaseModel):
    id: int
    passenger_name: str
    passenger_email: str
    route_name: str
    departure_time: datetime
    seats_booked: int
    booking_status: BookingStatus
    trip_status: TripStatus

    model_config = ConfigDict(from_attributes=True)