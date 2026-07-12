from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from database.session import SessionLocal
from models.user import User
from core.security import SECRET_KEY, ALGORITHM
from models.enums import UserRole

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token"
)


def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == email
    ).first()

    if user is None:
        raise credentials_exception

    return user

def get_current_admin(
    current_user: User = Depends(
        get_current_user
    )
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    return current_user

def get_current_driver(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.DRIVER:
        raise HTTPException(
            status_code=403,
            detail="Driver access required"
        )

    driver = current_user.driver

    if not driver:
        raise HTTPException(
            status_code=404,
            detail="Driver profile not found"
        )

    return driver