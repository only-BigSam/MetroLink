from pydantic import BaseModel


class RouteCreate(BaseModel):
    origin: str
    destination: str
    distance: float
    fare: float


class RouteResponse(BaseModel):
    id: int
    origin: str
    destination: str
    distance: float
    fare: float

    class Config:
        from_attributes = True