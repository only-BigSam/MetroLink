from fastapi import FastAPI

import models

from routes.auth import router as auth_router

app = FastAPI()

app.include_router(auth_router)