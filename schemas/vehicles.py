from pydantic import BaseModel, Field
from models.enums import VehicleStatus


class VehicleCreate(BaseModel):
    plate_number: str
    capacity: int


class VehicleResponse(BaseModel):
    id: int
    plate_number: str
    capacity: int = Field(ge=1, le=6)
    status: VehicleStatus

    class Config:
        from_attributes = True

class VehicleStatusUpdate(BaseModel):
    status: VehicleStatus