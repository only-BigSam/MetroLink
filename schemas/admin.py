from pydantic import BaseModel

class DashboardResponse(BaseModel):
    total_users: int
    total_drivers: int
    total_routes: int
    total_vehicles: int
    total_trips: int
    scheduled_trips: int
    active_trips: int
    completed_trips: int
    cancelled_trips: int
    total_bookings: int