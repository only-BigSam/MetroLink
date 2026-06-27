from pydantic import BaseModel


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