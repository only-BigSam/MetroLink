from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, UTC
from core.dependencies import get_current_admin, get_current_user
from database.session import get_db
from models.driver import Driver
from models.route import Route
from models.trip import Trip
from models.user import User, UserRole
from models.vehicle import Vehicle, VehicleStatus
from schemas.trip import TripCreate,TripResponse,TripStatus,TripStatusUpdate,AdminTripResponse,TripStatisticsResponse
from models.driver import Driver
from models.enums import BookingStatus
from sqlalchemy import func
from models.booking import Booking

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
    current_admin: User = Depends(get_current_admin)
):
    route = db.query(Route).filter(
        Route.id == trip_data.route_id
    ).first()

    if not route:
        raise HTTPException(
            status_code=404,
            detail="Route not found"
        )

    vehicle = db.query(Vehicle).filter(
        Vehicle.id == trip_data.vehicle_id
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )

    driver = db.query(Driver).filter(
        Driver.id == trip_data.driver_id
    ).first()

    if not driver:
        raise HTTPException(
            status_code=404,
            detail="Driver not found"
        )

    if trip_data.departure_time <= datetime.now(UTC):
        raise HTTPException(
            status_code=400,
            detail="Departure time must be in the future"
        )

    if trip_data.arrival_time <= trip_data.departure_time:
        raise HTTPException(
            status_code=400,
            detail="Arrival time must be after departure time"
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
            TripStatus.IN_TRANSIT
        ])
    ).first()

    if existing_trip:
        raise HTTPException(
            status_code=400,
            detail="Driver is already assigned to another trip"
        )

    existing_vehicle_trip = db.query(Trip).filter(
        Trip.vehicle_id == trip_data.vehicle_id,
        Trip.status.in_([
            TripStatus.SCHEDULED,
            TripStatus.IN_TRANSIT
        ])
    ).first()

    if existing_vehicle_trip:
        raise HTTPException(
            status_code=400,
            detail="Vehicle is already assigned to another trip"
        )

    new_trip = Trip(
        route_id=trip_data.route_id,
        vehicle_id=trip_data.vehicle_id,
        driver_id=trip_data.driver_id,
        departure_time=trip_data.departure_time,
        arrival_time=trip_data.arrival_time,
        status=TripStatus.SCHEDULED
    )

    db.add(new_trip)

    vehicle.status = VehicleStatus.IN_USE

    db.commit()
    db.refresh(new_trip)

    return new_trip

@router.get(
    "",
    response_model=list[AdminTripResponse]
)
def get_trips(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    trips = db.query(Trip).all()

    result = []

    for trip in trips:

        result.append(
            AdminTripResponse(
                id=trip.id,
                route=f"{trip.route.origin} → {trip.route.destination}",
                driver=trip.driver.user.name,
                vehicle=trip.vehicle.plate_number,
                departure_time=trip.departure_time,
                arrival_time=trip.arrival_time,
                status=trip.status
            )
        )

    return result

@router.get("/available")
def get_available_trips(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    trips = db.query(Trip).filter(
        Trip.status == TripStatus.SCHEDULED
    ).all()

    return [
        AdminTripResponse(
            id=trip.id,
            route=f"{trip.route.origin} → {trip.route.destination}",
            driver=trip.driver.user.name,
            vehicle=trip.vehicle.plate_number,
            departure_time=trip.departure_time,
            arrival_time=trip.arrival_time,
            status=trip.status
        )
        for trip in trips
    ]

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

@router.get(
    "/{trip_id}/statistics",
    response_model=TripStatisticsResponse
)
def get_trip_statistics(
    trip_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    trip = db.query(Trip).filter(
        Trip.id == trip_id
    ).first()

    if not trip:
        raise HTTPException(
            status_code=404,
            detail="Trip not found"
        )

    booked_seats = db.query(
        func.sum(Booking.seats_booked)
    ).filter(
        Booking.trip_id == trip_id,
        Booking.status.in_(
            [BookingStatus.CONFIRMED, BookingStatus.COMPLETED]
        )
    ).scalar() or 0

    total_bookings = db.query(Booking).filter(
        Booking.trip_id == trip_id
    ).count()

    return TripStatisticsResponse(
        trip_id=trip.id,
        trip_status=trip.status,
        vehicle_capacity=trip.vehicle.capacity,
        booked_seats=booked_seats,
        available_seats=trip.vehicle.capacity - booked_seats,
        total_bookings=total_bookings
    )