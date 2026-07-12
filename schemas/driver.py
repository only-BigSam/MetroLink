from pydantic import BaseModel, ConfigDict


class DriverCreate(BaseModel):
    user_id: int
    license_number: str
    phone_number: str


class DriverResponse(BaseModel):
    id: int
    user_id: int
    license_number: str
    phone_number: str

    class Config:
        from_attributes = True

class DriverResponse(BaseModel):
    id: int
    user_id: int
    name: str
    email: str
    license_number: str

    model_config = ConfigDict(from_attributes=True)