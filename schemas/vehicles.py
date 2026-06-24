from pydantic import BaseModel
from models.enums import VehicleStatus


class VehicleCreate(BaseModel):
    plate_number: str
    capacity: int


class VehicleResponse(BaseModel):
    id: int
    plate_number: str
    capacity: int
    status: VehicleStatus

    class Config:
        from_attributes = True