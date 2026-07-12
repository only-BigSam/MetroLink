from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.booking import Booking
from core.dependencies import get_current_admin
from database.session import get_db
from models.driver import Driver
from models.enums import UserRole
from models.user import User
from schemas.driver import DriverCreate, DriverResponse
from schemas.booking import DriverPassengerResponse, TripPassengerResponse
from core.dependencies import get_current_admin, get_current_user, get_current_driver
from models.trip import Trip
from models.enums import BookingStatus
from schemas.trip import DriverTripResponse
from schemas.trip import TripStatus
from datetime import datetime,UTC
from models.vehicle import VehicleStatus

router = APIRouter(
    prefix="/drivers",
    tags=["Drivers"]
)

@router.post(
    "",
    response_model=DriverResponse
)
def create_driver(
    driver_data: DriverCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(
        get_current_admin
    )
):
    user = db.query(User).filter(
        User.id == driver_data.user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    if user.role != UserRole.DRIVER:
        raise HTTPException(
            status_code=400,
            detail="User is not a driver"
        )
    
    existing_driver = db.query(Driver).filter(
    Driver.user_id == driver_data.user_id
    ).first()

    if existing_driver:
        raise HTTPException(
            status_code=400,
            detail="Driver already exists"
        )
    
    new_driver = Driver(
    user_id=driver_data.user_id,
    license_number=driver_data.license_number,
    phone_number=driver_data.phone_number)

    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)

    return new_driver

@router.get("/{trip_id}/passengers", response_model=list[TripPassengerResponse])
def get_trip_passengers(
    trip_id: int,
    db: Session = Depends(get_db),
    current_driver: Driver = Depends(get_current_driver)
):
    trip = db.query(Trip).filter(
        Trip.id == trip_id
    ).first()

    if not trip:
        raise HTTPException(
            status_code=404,
            detail="Trip not found"
        )

    if trip.driver_id != current_driver.id:
        raise HTTPException(
            status_code=403,
            detail="You are not assigned to this trip"
        )

    bookings = db.query(Booking).filter(
        Booking.trip_id == trip_id
    ).all()

    return [
        TripPassengerResponse(
            booking_id=booking.id,
            passenger_name=booking.user.name,
            passenger_email=booking.user.email,
            seats_booked=booking.seats_booked
        )
        for booking in bookings
    ]
@router.get(
    "/drivers/trips/{trip_id}/passengers",
    response_model=list[DriverPassengerResponse]
)
def get_trip_passengers(
    trip_id: int,
    db: Session = Depends(get_db),
    current_driver: Driver = Depends(get_current_driver)
):
    trip = db.query(Trip).filter(
        Trip.id == trip_id
    ).first()

    if not trip:
        raise HTTPException(
            status_code=404,
            detail="Trip not found"
        )

    if trip.driver_id != current_driver.id:
        raise HTTPException(
            status_code=403,
            detail="You are not assigned to this trip"
        )

    bookings = db.query(Booking).filter(
        Booking.trip_id == trip_id
    ).all()

    return [
        DriverPassengerResponse(
            booking_id=booking.id,
            passenger_name=booking.user.name,
            passenger_email=booking.user.email,
            seats_booked=booking.seats_booked,
            booking_status=booking.status
        )
        for booking in bookings
    ]

@router.get(
    "/drivers/me/trips",
    response_model=list[DriverTripResponse]
)
def get_my_trips(
    db: Session = Depends(get_db),
    current_driver: Driver = Depends(get_current_driver)
):
    trips = db.query(Trip).filter(
        Trip.driver_id == current_driver.id
    ).all()

    return [
        DriverTripResponse(
            trip_id=trip.id,
            route_name=f"{trip.route.origin} → {trip.route.destination}",
            departure_time=trip.departure_time,
            arrival_time=trip.arrival_time,
            vehicle_number=trip.vehicle.plate_number,
            trip_status=trip.status
        )
        for trip in trips
    ]
@router.patch("/{trip_id}/start")
def start_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    current_driver: User = Depends(get_current_driver)
):
    trip = db.query(Trip).filter(
        Trip.id == trip_id
    ).first()

    if not trip:
        raise HTTPException(
            status_code=404,
            detail="Trip not found"
        )

    if trip.driver_id != current_driver.id:
        raise HTTPException(
            status_code=403,
            detail="You are not assigned to this trip"
        )

    if trip.status != TripStatus.SCHEDULED:
        raise HTTPException(
            status_code=400,
            detail="Trip cannot be started"
        )

    current_time = datetime.now()

    if current_time < trip.departure_time:
        raise HTTPException(
            status_code=400,
            detail="You cannot start this trip before its scheduled departure time."
        )

    trip.status = TripStatus.IN_TRANSIT
    trip.vehicle.status = VehicleStatus.IN_USE

    db.commit()
    db.refresh(trip)

    return {
        "message": "Trip started successfully",
        "trip_status": trip.status
    }

@router.patch("/{trip_id}/complete")
def complete_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    current_driver: Driver = Depends(get_current_driver)
):
    trip = db.query(Trip).filter(
        Trip.id == trip_id
    ).first()

    if not trip:
        raise HTTPException(
            status_code=404,
            detail="Trip not found"
        )

    if trip.driver_id != current_driver.id:
        raise HTTPException(
            status_code=403,
            detail="You are not assigned to this trip"
        )

    if trip.status != TripStatus.IN_TRANSIT:
        raise HTTPException(
            status_code=400,
            detail="Only trips in transit can be completed"
        )

    trip.status = TripStatus.COMPLETED
    trip.vehicle.status = VehicleStatus.AVAILABLE

    bookings = db.query(Booking).filter(
        Booking.trip_id == trip.id,
        Booking.status == BookingStatus.CONFIRMED
    ).all()

    for booking in bookings:
        booking.status = BookingStatus.COMPLETED

    db.commit()
    db.refresh(trip)

    return {
        "message": "Trip completed successfully",
        "trip_status": trip.status
    }

@router.get("/", response_model=list[DriverResponse])
def get_all_drivers(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    drivers = db.query(Driver).all()

    return [
        DriverResponse(
            id=driver.id,
            user_id=driver.user_id,
            name=driver.user.name,
            email=driver.user.email,
            license_number=driver.license_number
        )
        for driver in drivers
    ]