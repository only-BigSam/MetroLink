from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.dependencies import get_current_admin
from database.session import get_db
from models.enums import VehicleStatus
from models.user import User
from models.vehicle import Vehicle
from schemas.vehicles import VehicleCreate, VehicleResponse

router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"]
)

@router.post(
    "",
    response_model=VehicleResponse
)
def create_vehicle(
    vehicle_data: VehicleCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(
        get_current_admin
    )
):
    existing_vehicle = db.query(
    Vehicle
    ).filter(Vehicle.plate_number == vehicle_data.plate_number).first()

    if existing_vehicle:
        raise HTTPException(
            status_code=400,
            detail="Vehicle already exists")
    
    new_vehicle = Vehicle(
    plate_number=vehicle_data.plate_number,
    capacity=vehicle_data.capacity,
    status=VehicleStatus.AVAILABLE)
    
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)

    return new_vehicle
