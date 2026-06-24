from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.dependencies import get_current_admin
from database.session import get_db
from models.enums import VehicleStatus
from models.user import User
from models.vehicle import Vehicle
from schemas.vehicles import VehicleCreate, VehicleResponse, VehicleStatusUpdate

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

@router.get(
    "",
    response_model=list[VehicleResponse]
)
def get_vehicles(
    db: Session = Depends(get_db),
    current_admin: User = Depends(
        get_current_admin
    )
):
    vehicles = db.query(
        Vehicle
    ).all()

    return vehicles

@router.get(
    "/{vehicle_id}",
    response_model=VehicleResponse
)
def get_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(
        get_current_admin
    )
):
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == vehicle_id).first()

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )

    return vehicle

@router.patch(
    "/{vehicle_id}/status",
    response_model=VehicleResponse
)
def update_vehicle_status(
    vehicle_id: int,
    status_data: VehicleStatusUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(
        get_current_admin
    )
):
    vehicle = db.query(Vehicle).filter(
    Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )

    vehicle.status = status_data.status

    db.commit()
    db.refresh(vehicle)

    return vehicle