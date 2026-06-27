from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.dependencies import get_current_admin
from database.session import get_db
from models.driver import Driver
from models.enums import UserRole
from models.user import User
from schemas.driver import DriverCreate, DriverResponse

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