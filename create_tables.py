from database.base import Base
from database.connection import engine

from models.user import User
from models.driver import Driver
from models.vehicle import Vehicle
from models.route import Route
from models.trip import Trip
from models.booking import Booking

Base.metadata.create_all(bind=engine)

print("Tables created successfully.")