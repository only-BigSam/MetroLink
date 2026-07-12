from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.session import get_db
from core.dependencies import get_current_admin

from models.user import User
from models.driver import Driver
from models.route import Route
from models.vehicle import Vehicle
from models.trip import Trip
from models.booking import Booking
from schemas.booking import AdminBookingResponse
from schemas.admin import DashboardResponse
from schemas.trip import AdminTripResponse
from models.enums import TripStatus


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get(
    "/data",
    response_model=DashboardResponse
)
def get_all_data(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    total_users = db.query(User).count()

    total_drivers = db.query(Driver).count()

    total_routes = db.query(Route).count()

    total_vehicles = db.query(Vehicle).count()

    total_trips = db.query(Trip).count()

    scheduled_trips = db.query(Trip).filter(
        Trip.status == TripStatus.SCHEDULED
    ).count()

    active_trips = db.query(Trip).filter(
        Trip.status == TripStatus.IN_TRANSIT
    ).count()

    completed_trips = db.query(Trip).filter(
        Trip.status == TripStatus.COMPLETED
    ).count()

    cancelled_trips = db.query(Trip).filter(
        Trip.status == TripStatus.CANCELLED
    ).count()

    total_bookings = db.query(Booking).count()

    return DashboardResponse(
        total_users=total_users,
        total_drivers=total_drivers,
        total_routes=total_routes,
        total_vehicles=total_vehicles,
        total_trips=total_trips,
        scheduled_trips=scheduled_trips,
        active_trips=active_trips,
        completed_trips=completed_trips,
        cancelled_trips=cancelled_trips,
        total_bookings=total_bookings
    )

@router.get(
    "/trips",
    response_model=list[AdminTripResponse]
)
def get_all_trips(
    status: TripStatus | None = None,
    driver_id: int | None = None,
    vehicle_id: int | None = None,
    route_id: int | None = None,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    query = db.query(Trip)
    if status:
        query = query.filter(
            Trip.status == status)

    if driver_id:
        query = query.filter(
            Trip.driver_id == driver_id)

    if vehicle_id:
        query = query.filter(
            Trip.vehicle_id == vehicle_id)

    if route_id:
        query = query.filter(
            Trip.route_id == route_id)
    
    trips = query.all()
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