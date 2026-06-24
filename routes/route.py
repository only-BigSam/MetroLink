from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.dependencies import get_current_admin
from database.session import get_db
from models.route import Route
from models.user import User
from schemas.route import RouteCreate, RouteResponse

router = APIRouter(
    prefix="/routes",
    tags=["Routes"]
)

@router.post(
    "",
    response_model=RouteResponse
)
def create_route(
    route_data: RouteCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(
        get_current_admin
    )
):
    new_route = Route(
    origin=route_data.origin,
    destination=route_data.destination,
    distance=route_data.distance,
    fare=route_data.fare
)
    db.add(new_route)
    db.commit()
    db.refresh(new_route)

    return new_route

@router.get(
    "",
    response_model=list[RouteResponse]
)
def get_routes(
    db: Session = Depends(get_db),
    current_admin: User = Depends(
        get_current_admin
    )
):
    routes = db.query(
        Route
    ).all()

    return routes

@router.get(
    "/{route_id}",
    response_model=RouteResponse
)
def get_route(
    route_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(
        get_current_admin
    )
):
    route = db.query(
        Route
    ).filter(
        Route.id == route_id
    ).first()

    if not route:
        raise HTTPException(
            status_code=404,
            detail="Route not found"
        )

    return route