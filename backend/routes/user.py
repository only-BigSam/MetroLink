from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.dependencies import get_current_admin
from database.session import get_db
from models.enums import UserRole
from models.user import User
from schemas.user import UserResponse
from schemas.user import UserResponse, UserRoleUpdate

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get(
    "",
    response_model=list[UserResponse]
)
def get_users(
    db: Session = Depends(get_db),
    current_admin: User = Depends(
        get_current_admin
    )
):
    
    users = db.query(User).all()

    return users

@router.patch(
    "/{user_id}/role",
    response_model=UserResponse
)
def update_user_role(
    user_id: int,
    role_data: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(
        get_current_admin
    )
):
    user = db.query(User).filter(
    User.id == user_id
).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.role = role_data.role

    db.commit()
    db.refresh(user)

    return user