from datetime import datetime

from pydantic import BaseModel

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