from fastapi import FastAPI
import models
from routes.auth import router as auth_router
from routes.vehicle import router as vehicle_router
from routes.route import router as route_router
from routes.trip import router as trip_router
from routes.driver import router as driver_router
from routes.user import router as user_router
from routes.booking import router as booking_router
import uvicorn

app = FastAPI()

app.include_router(auth_router)
app.include_router(vehicle_router)
app.include_router(route_router)
app.include_router(trip_router)
app.include_router(driver_router)
app.include_router(user_router)
app.include_router(booking_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )