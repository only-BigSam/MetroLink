from fastapi import FastAPI
import models
from routes.auth import router as auth_router
from routes.vehicle import router as vehicle_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(vehicle_router)