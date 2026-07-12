from datetime import datetime

from backend.database.session import SessionLocal

from backend.models.user import User
from backend.models.driver import Driver
from backend.models.vehicle import Vehicle
from backend.models.route import Route
from backend.models.trip import Trip
from backend.models.booking import Booking

from backend.models.enums import (
    UserRole,
    VehicleStatus,
    TripStatus,
    BookingStatus
)


db = SessionLocal()

# Creating Driver
driver_user = User(
    name="David",
    email="david@example.com",
    password_hash="hashed_password",
    role=UserRole.DRIVER
)

db.add(driver_user)
db.commit()
db.refresh(driver_user)

# Creating Driver's Profile
driver = Driver(
    user_id=driver_user.id,
    license_number="LIC12345",
    phone_number="08012345678"
)

db.add(driver)
db.commit()
db.refresh(driver)

# Creating Passenger
passenger = User(
    name="John",
    email="john@example.com",
    password_hash="hashed_password",
    role=UserRole.PASSENGER
)

db.add(passenger)
db.commit()
db.refresh(passenger)

# Creating Vehicle
vehicle = Vehicle(
    plate_number="ABC-123",
    capacity=4,
    status=VehicleStatus.AVAILABLE
)

db.add(vehicle)
db.commit()
db.refresh(vehicle)

# Creating Route
route = Route(
    origin="Abuja",
    destination="Lagos",
    distance=750.5,
    fare=15000
)

db.add(route)
db.commit()
db.refresh(route)

# Creating Trip
trip = Trip(
    route_id=route.id,
    vehicle_id=vehicle.id,
    driver_id=driver.id,
    departure_time=datetime.now(),
    arrival_time=datetime.now(),
    status=TripStatus.SCHEDULED
)

db.add(trip)
db.commit()
db.refresh(trip)

# Creating Booking
booking = Booking(
    user_id=passenger.id,
    trip_id=trip.id,
    status=BookingStatus.CONFIRMED
)

db.add(booking)
db.commit()

print("Database test completed successfully!")

db.close()