from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.dependencies import get_current_admin, get_current_user
from database.session import get_db
from models.driver import Driver
from models.route import Route
from models.trip import Trip
from models.user import User, UserRole
from models.vehicle import Vehicle, VehicleStatus
from schemas.trip import TripCreate, TripResponse, TripStatus, TripStatusUpdate

router = APIRouter(
    prefix="/trips",
    tags=["Trips"]
)

@router.post(
    "",
    response_model=TripResponse
)
def create_trip(
    trip_data: TripCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(
        get_current_admin
    )
):
    route = db.query(Route).filter(
    Route.id == trip_data.route_id).first()

    if not route:
        raise HTTPException(
            status_code=404,
            detail="Route not found"
        )
    
    vehicle = db.query(Vehicle).filter(
    Vehicle.id == trip_data.vehicle_id).first()

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )
    
    driver = db.query(Driver).filter(
    Driver.id == trip_data.driver_id).first()

    if not driver:
        raise HTTPException(
            status_code=404,
            detail="Driver not found"
        )
    
    if vehicle.status != VehicleStatus.AVAILABLE:
        raise HTTPException(
        status_code=400,
        detail="Vehicle is not available"
    )

    existing_trip = db.query(Trip).filter(
    Trip.driver_id == trip_data.driver_id,
    Trip.status.in_([
        TripStatus.SCHEDULED,
        TripStatus.IN_TRANSIT])).first()

    if existing_trip:
        raise HTTPException(
            status_code=400,
            detail="Driver is already assigned to another trip"
        )

    new_trip = Trip(
    route_id=trip_data.route_id,
    vehicle_id=trip_data.vehicle_id,
    driver_id=trip_data.driver_id,
    departure_time=trip_data.departure_time,
    arrival_time=trip_data.arrival_time)

    db.add(new_trip)

    vehicle.status = VehicleStatus.IN_USE

    db.commit()
    db.refresh(new_trip)

    return new_trip

@router.get(
    "",
    response_model=list[TripResponse]
)
def get_trips(
    db: Session = Depends(get_db),
    current_admin: User = Depends(
        get_current_admin
    )
):
    trips = db.query(Trip).all()

    return trips

@router.get(
    "/{trip_id}",
    response_model=TripResponse
)
def get_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(
        get_current_admin
    )
):
    trip = db.query(Trip).filter(
        Trip.id == trip_id
    ).first()

    if not trip:
        raise HTTPException(
            status_code=404,
            detail="Trip not found"
        )

    return trip

@router.patch(
    "/{trip_id}/status",
    response_model=TripResponse
)
def update_trip_status(
    trip_id: int,
    status_data: TripStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    trip = db.query(Trip).filter(
    Trip.id == trip_id).first()

    if not trip:
        raise HTTPException(
            status_code=404,
            detail="Trip not found"
        )

    if (current_user.role != UserRole.ADMIN
        and current_user.id != trip.driver.user_id
    ):
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to update this trip"
        )

    trip.status = status_data.status

    if status_data.status in [
        TripStatus.COMPLETED,
        TripStatus.CANCELLED
    ]:
        trip.vehicle.status = VehicleStatus.AVAILABLE

    db.commit()
    db.refresh(trip)

    return trip