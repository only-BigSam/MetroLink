from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.user import UserLogin, UserRegister, UserResponse
from core.security import verify_password, create_access_token, hash_password
from database.session import get_db
from models.user import User
from models.enums import UserRole
from schemas.user import UserRegister, UserResponse
from core.security import hash_password
from core.dependencies import get_current_admin, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Header

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.get("/token-test")
def token_test(
    authorization: str | None = Header(default=None)
):
    return {
        "authorization": authorization
    }

@router.post("/token")
def login_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == form_data.username.lower()
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        form_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={
            "sub": user.email,
            "role": user.role.value
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/test")
def test_auth():
    return {
        "message": "Auth route working"
    }

@router.post(
    "/register",
    response_model=UserResponse
)
def register_user(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    email = user_data.email.lower()
    existing_user = db.query(User).filter(
    User.email == email
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    hashed_password = hash_password(
    user_data.password
)
    new_user = User(
    name=user_data.name,
    email=email,
    password_hash=hashed_password,
    role=UserRole.PASSENGER
)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login")
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
    User.email == user_data.email.lower()
    ).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    if not verify_password(
    user_data.password,
    user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    access_token = create_access_token(
    data={
        "sub": user.email,
        "role": user.role.value
    }
    )
    return {
    "access_token": access_token,
    "token_type": "bearer"
}

@router.get("/protected-test")
def protected_test(
    current_user: User = Depends(
        get_current_user
    )
):
    return {
        "email": current_user.email,
        "role": current_user.role.value
    }

@router.get("/admin-test")
def admin_test(
    current_admin: User = Depends(
        get_current_admin
    )
):
    return {
        "message": "Welcome Admin",
        "email": current_admin.email
    }