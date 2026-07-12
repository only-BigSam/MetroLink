from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from database.session import get_db
from core.dependencies import get_current_user, get_current_admin

from models.booking import Booking
from models.trip import Trip
from models.user import User
from models.enums import BookingStatus, TripStatus

from schemas.booking import BookingCreate, BookingResponse, BookingDetailedResponse, AdminBookingResponse

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)

@router.post(
    "",
    response_model=BookingResponse
)
def create_booking(
    booking_data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    
    trip = db.query(Trip).filter(
    Trip.id == booking_data.trip_id).first()

    if not trip:
        raise HTTPException(
            status_code=404,
            detail="Trip not found")
    
    if trip.status != TripStatus.SCHEDULED:
        raise HTTPException(
            status_code=400,
            detail="This trip is not available for booking")
    
    if trip.departure_time <= datetime.now():
        raise HTTPException(
            status_code=400,
            detail="This trip has already departed")
    
    if booking_data.seats_booked <= 0:
        raise HTTPException(
            status_code=400,
            detail="Seats booked must be at least 1")
    
    booked_seats = db.query(
    func.sum(Booking.seats_booked)
    ).filter(
        Booking.trip_id == booking_data.trip_id,
        Booking.status == BookingStatus.CONFIRMED
    ).scalar() or 0

    remaining_seats = (
    trip.vehicle.capacity - booked_seats)

    if booking_data.seats_booked > remaining_seats:
        raise HTTPException(
            status_code=400,
            detail=f"{remaining_seats} seats remaining")
    
    new_booking = Booking(
    user_id=current_user.id,
    trip_id=booking_data.trip_id,
    seats_booked=booking_data.seats_booked)

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return new_booking

@router.get(
    "/me",
    response_model=list[BookingDetailedResponse]
)
def get_my_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bookings = db.query(Booking).filter(
        Booking.user_id == current_user.id
    ).all()

    return [
    BookingDetailedResponse(
        id=booking.id,
        trip_id=booking.trip_id,
        seats_booked=booking.seats_booked,
        status=booking.status,
        departure_time=booking.trip.departure_time,
        arrival_time=booking.trip.arrival_time,
        route_name=f"{booking.trip.route.origin} → {booking.trip.route.destination}",
        vehicle_number=booking.trip.vehicle.plate_number,
        trip_status=booking.trip.status
    )
    for booking in bookings
]

@router.get(
    "/",
    response_model=list[AdminBookingResponse]
)
def get_all_bookings(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    bookings = db.query(Booking).all()

    return [
        AdminBookingResponse(
            id=booking.id,
            passenger_name=booking.user.name,
            passenger_email=booking.user.email,
            route_name=f"{booking.trip.route.origin} → {booking.trip.route.destination}",
            departure_time=booking.trip.departure_time,
            seats_booked=booking.seats_booked,
            booking_status=booking.status,
            trip_status=booking.trip.status
        )
        for booking in bookings
    ]

@router.patch("/{booking_id}/cancel")
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    if booking.status == BookingStatus.CANCELLED:
        raise HTTPException(
            status_code=400,
            detail="Booking has already been cancelled"
        )

    if booking.trip.status == TripStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail="Cannot cancel a booking for a completed trip"
        )

    booking.status = BookingStatus.CANCELLED

    db.commit()
    db.refresh(booking)

    return {
        "message": "Booking cancelled successfully"
    }